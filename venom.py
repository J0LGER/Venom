#!/usr/bin/env python3 
from flask import *
from argparse import ArgumentParser 
import controllers.db
from http.server import HTTPServer
from controllers.listener import Listener 
import time
from threading import Thread 

if __name__ == "__main__": 
    
    app = Flask(__name__) 
    @app.route('/', methods = ['GET']) 
    def index(): 
        return render_template('index.html') 


    @app.route('/login', methods = ['POST'])
    def authenticate(): 
        print('JWT Handler') 


    @app.route('/listeners', methods = ['GET','POST'])  
    def listeners(): 
        if (request.method == 'GET'):
            return 'List Listeners with their status'      
        elif (request.method == 'POST'): 
            print('PORT:' + str(request.form.get('port')))
            httpd = HTTPServer(('0.0.0.0', int(request.form.get('port'))), Listener)
            print(time.asctime(), "Start Server - %s:%s"%('0.0.0.0', str(request.form.get('port'))))
            try:
                listener = Thread(target= httpd.serve_forever) 
                listener.daemon = True
                listener.start()
                #httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            #This method is used to terminate the listener object
            #httpd.server_close()
            print(time.asctime(), "Stop Server - %s:%s"%('0.0.0.0', str(request.form.get('port'))))
        return 'Listener spawned'

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





 










        