#!/usr/bin/env python3 
from flask import *
from argparse import ArgumentParser 
from controllers.db import * 
from http.server import HTTPServer
from controllers.listener import Listener 
import time
from threading import Thread
from random import choices 
from string import ascii_uppercase , digits
import jwt 
from hashlib import sha256
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

''' TO DO: 
1- Implement a one time registration feature
2- Intergrate a good unified success/error handling in all test cases
''' 

if __name__ == "__main__": 
    
    app = Flask(__name__)    
    app.config['MONGODB_SETTINGS'] = {
                 'db': 'users',
                 'host': 'localhost',
                 'port': 27017		 } 
    
    _SECRET_ = "".join(choices(ascii_uppercase + digits, k = 20))
    _LISTENERS_ = dict()

    @app.route('/', methods = ['GET']) 
    def index(): 
        return render_template('index.html') 


    @app.route('/login', methods = ['POST'])
    def authenticate(): 
        print('JWT Handler') 
        

    @app.route('/listeners', methods = ['GET','POST'])  
    def listeners(): 
            if(request.method == 'GET'):
                return 'List Listeners with their status'      
            
            elif (request.method == 'POST'): 
                if (request.form.get('action') == 'create' and request.form.get('port')): 
                    try:
                        id = "".join(choices(digits, k = 5))    
                        port = int(request.form.get('port'))
                        _LISTENERS_["listener_%s" % id] = HTTPServer(('0.0.0.0', port), Listener)
                        #----------------------------------------------------------------------
                        AESKey = os.urandom(16)
                        #----------------------------------------------------------------------
                        saveListener(id, port, AESKey)    
                        listener = Thread(target = _LISTENERS_["listener_%s" % id].serve_forever) 
                        listener.daemon = True
                        listener.start()
                        print(time.asctime(), "Start Server - %s:%s"%('0.0.0.0', str(request.form.get('port'))))

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

    @app.route('/agents', methods = ['GET']) 
    def agents(): 


        return 'Some code' 

    @app.route('/implant', methods = ['GET','POST']) 
    def implant():
        if (request.method == 'GET'):
            return 'return an implant template to allow users create their implants'      
        elif (request.method == 'POST'): 
            return 'An implant file in response'
    
    parser = ArgumentParser(description='Welcome to VENOM') 
    parser.add_argument('--port', type=int, required=True, default='8080', help='Port number, Default set to 8080 ') 
    args = parser.parse_args() 
    app.run(host='0.0.0.0', port=args.port, debug=True)
    #if(db.venom.find_one({'username': {'$eq': 'admin' }, 'password': {'$eq': "admin".encode('utf-8').hexdigest()} })): 
     #   _REG_FLAG_ = 1 
    #else: 
     #   db.venom.insert({'username': {'$eq': 'admin' }, 'password': {'$eq': "admin".encode('utf-8').hexdigest()} }))
      #  _REG_FLAG_ = 0
            
