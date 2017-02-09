#!/usr/bin/env python
import os
import re
import sys
import logging
import fnmatch  
import importlib
import argparse	
import json
from flask import request
from flask import Flask
from flask import jsonify
from time import gmtime, strftime


# import archive handlers
# this python library path
PATH = str(os.path.dirname(os.path.abspath(__file__)))

# the path to the handlers scripts
PATH_HANDLER = PATH + '/handlers/'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/archivenow_debug.log',
                    filemode='w')

# for the web app
app = Flask(__name__)

# create handlers for enabled archives
global handlers
handlers = {}

# defult value for server/port
SERVER_IP = 'localhost'
SERVER_PORT = 12345


def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Error in processing the request',
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

def getServer_IP_PORT():
	u = str(SERVER_IP)
	if str(SERVER_PORT) != '80':
		u = u + ":"+str(SERVER_PORT)
	if 'http' != u[0:4]:
		u = 'http://' + u
	return u


def listArchives_server(handlers):

	li = {"archives": [{"id":"all","post":getServer_IP_PORT()+'/all/'+'{URI}',"archive-name":"All enabled archives"}] }
	for handler in handlers:
		li["archives"].append({"id":handler,"archive-name":handlers[handler].name,
			"post":getServer_IP_PORT()+'/'+handler+'/'+'{URI}'})
	return 	li					

# GET
@app.route('/')
def index():
	strTprint = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - '
	strTprint += str(request.remote_addr) + ' - '
	new_url = str(request.url).split(getServer_IP_PORT(),1)
	if len(new_url) > 1:
		strTprint += new_url[1] + ' - '
	else:
		strTprint += request.url + ' - '	
	resp = jsonify(listArchives_server(handlers))
	resp.status_code = 200	
	print  strTprint+str(' 200')
	return resp

#POST
@app.route('/<path:tmp>', methods=['GET'])
def pushit(tmp):
	try:
		strTprint = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' - '
		strTprint += str(request.remote_addr) + ' - '
		new_url = str(request.url).split(getServer_IP_PORT(),1)
		if len(new_url) > 1:
			strTprint += new_url[1] + ' - '
		else:
			strTprint += request.url + ' - '

		allurl = str(request.url)
		s = allurl.split(getServer_IP_PORT()+'/',1)[1].split('/',1)	
		arc_id = s[0]
		URI = s[1] 

		# to push into archives
		resp = {"results":push(URI, arc_id)}

		if len(resp["results"]) == 0:
			print  strTprint+str(' 400')
			return bad_request();
		else:				
		# what should be return
			resp = jsonify(resp)
			print  strTprint+str(' 200')
			resp.status_code = 200
			#resp.headers['Location'] = getServer_IP_PORT()+ timeSpecificURI;	
			return resp;
	except Exception as e:
		print  strTprint+str(' 400')
		logging.error(e)
		pass;
	return bad_request();

def push(URI,arc_id):
	global handlers
	try:
		# push to all possible archives
		res = []
		if arc_id == 'all':
			for handler in handlers:
				handlers[handler].push(str(URI))
				res.append(handlers[handler].urim)
		else:
			# push to the chosen archives 
			for handler in handlers:
				if arc_id == handler:
					handlers[handler].push(str(URI))
					res.append(handlers[handler].urim)
		return res
	except Exception as e:
		logging.error(e)
		pass;
	return []

def start(port=SERVER_PORT):
	global SERVER_PORT
	SERVER_PORT = port
	print '\n'+strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\nRunning on '+getServer_IP_PORT()+'\n(Press CTRL+C to quit) \n'
	app.run(host=SERVER_IP, port=port, threaded=True, debug=True, use_reloader=False)  


def load_handlers():
	global handlers
	handlers = {}
	# add the path of the handlers to the system so they can be imported
	#sys.path.insert(0, PATH_HANDLER)
	sys.path.append(PATH_HANDLER)

	# create a list of handlers. 
	# Ex. handlers['IA'] is an object of the class IA_handler in the module ia_handler.py
	for file in os.listdir(PATH_HANDLER):
		# all filenames end with .py
		if fnmatch.fnmatch(file, "*.py"):
			sfile = file.split('_',1)
			if len(sfile) == 2:
				if sfile[1] == 'handler.py':
					# the string before _ must conatins digits and/or numbers only
					if re.match("^[A-Za-z0-9_-]*$", sfile[0]):
						#print PATH_HANDLER+'/'+file[:-3]
						#mod = importlib.import_module(PATH_HANDLER+'/'+file[:-3])
						mod = importlib.import_module(file[:-3]) 
						mod_class = getattr(mod, sfile[0].upper()+'_handler')
						# finally an object is created of a class; use .name .push ...
						handlers[sfile[0]] = mod_class()
						if not handlers[sfile[0]].enabled:
							del handlers[sfile[0]]


def args_parser():
	global SERVER_PORT 
	# parsing arguments 
	class MyParser(argparse.ArgumentParser):
	    def error(self, message):
	        sys.stderr.write('error: %s\n' % message)
	        self.print_help()
	        sys.exit(2)

	    def printm(self):
	        sys.stderr.write('')
	        self.print_help()
	        sys.exit(2)

	parser=MyParser()

	arc_handler = 0
	for handler in handlers:
		# add archives identifiers to the list of options
		arc_handler += 1
		parser.add_argument('--'+handler,  action='store_true', default=False, 
   	                        help='Use '+handlers[handler].name)
	if arc_handler > 0:
		parser.add_argument('--all',  action='store_true', default=False, 
	                         help='Use all possible archives ')

		parser.add_argument('--server',  action='store_true', default=False, 
	                         help='Run archiveNow as a Web Service ')		

		parser.add_argument('URI', nargs='?', help='URI of a web resource')

		parser.add_argument('--port', nargs='?', help='port number to run a Web Service')

		args=parser.parse_args()
	else:
		print 'No enabled archive handler found'	

	arc_opt = 0;

	if getattr(args, 'server'):
		if getattr(args, 'port'):
			SERVER_PORT = int(args.port)

		start(port=SERVER_PORT)

	else: 
		if not getattr(args, 'URI'):
			print parser.error('too few arguments')
		res = []	
		# push to all possible archives
		if getattr(args, 'all'):
			arc_opt = 1
			res = push(str(args.URI),'all')
		else:
			# push to the chosen archives 
			for handler in handlers:
				if getattr(args, handler):
					arc_opt += 1
					for i in push(str(args.URI),handler):
						res.append(i)
		if (arc_handler > 0) and (arc_opt == 0):
			print parser.printm()
		else:
			print res	

load_handlers();

if __name__ == '__main__':
    args_parser();


