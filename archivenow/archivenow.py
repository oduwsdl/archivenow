#!/usr/bin/env python
import os
import re
import sys
import uuid
import glob
import json
import importlib
import argparse
import string
from threading import Thread
from flask import request, Flask, jsonify, render_template
from pathlib import Path

#from __init__ import __version__ as archiveNowVersion

archiveNowVersion = '2019.2.24.11.10.10'

# archive handlers path
PATH = Path(os.path.dirname(os.path.abspath(__file__)))
PATH_HANDLER = PATH / 'handlers'

# for the web app
app = Flask(__name__)

# create handlers for enabled archives
global handlers
handlers = {}

# defult value for server/port
SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345


def bad_request(error=None):
    message = {
        'status': 400,
        'message': 'Error in processing the request',
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp


# def getServer_IP_PORT():
#     u = str(SERVER_IP)
#     if str(SERVER_PORT) != '80':
#         u = u + ":" + str(SERVER_PORT)
#     if 'http' != u[0:4]:
#         u = 'http://' + u
#     return u


def listArchives_server(handlers):
    uri_args = ''
    if 'cc' in handlers:
        if handlers['cc'].enabled and handlers['cc'].api_required:
            uri_args = '?cc_api_key={Your-Perma.cc-API-Key}'
    li = {"archives": [{  # getServer_IP_PORT() + 
        "id": "all", "GET":'/all/' + '{URI}'+uri_args,
        "archive-name": "All enabled archives"}]}
    for handler in handlers:
        if handlers[handler].enabled:
            uri_args2 = ''
            if handler == 'cc':
                uri_args2 = uri_args
            li["archives"].append({ #getServer_IP_PORT() +
                "id": handler, "archive-name": handlers[handler].name,
                "GET":  '/' + handler + '/' + '{URI}'+uri_args2})
    return li


@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def pushit(path):
    # no path; return a list of avaliable archives
    if path == '':
        #resp = jsonify(listArchives_server(handlers))
        #resp.status_code = 200
        return render_template('index.html')
        #return resp
    # get request with path
    elif (path == 'api'):
        resp = jsonify(listArchives_server(handlers))
        resp.status_code = 200
        return resp
    elif (path == "ajax-loader.gif"):
        return render_template('ajax-loader.gif')
    else:
        try:
            # get the args passed to push function like API KEY if provided
            PUSH_ARGS = {}
            for k in request.args.keys():
                PUSH_ARGS[k] = request.args[k]

            s = str(path).split('/', 1)
            arc_id = s[0]
            URI = request.url.split('/', 4)[4] # include query params, too

            if 'herokuapp.com' in request.host:
                PUSH_ARGS['from_heroku'] = True

            # To push into archives
            resp = {"results": push(URI, arc_id, PUSH_ARGS)}
            if len(resp["results"]) == 0:
                return bad_request()
            else:
                # what to return
                resp = jsonify(resp)
                resp.status_code = 200

                return resp
        except Exception as e:
            pass
        return bad_request()

res_uris = {}


def push_proxy(hdlr, URIproxy, p_args_proxy, res_uris_idx):
    global res_uris
    try:
        res = hdlr.push( URIproxy , p_args_proxy)
        print ( res )
        res_uris[res_uris_idx].append(res)
    except:
        pass;

def push(URI, arc_id, p_args={}):
    global handlers
    global res_uris
    try:
        # push to all possible archives
        res_uris_idx = str(uuid.uuid4())
        res_uris[res_uris_idx] = []
        ### if arc_id == 'all':
            ### for handler in handlers:
                ### if (handlers[handler].api_required):
                    # pass args like key API
                    ### res.append(handlers[handler].push(str(URI), p_args))
                ### else:
                    ### res.append(handlers[handler].push(str(URI)))
        ### else:
            # push to the chosen archives

        threads = []

        for handler in handlers:
            if (arc_id == handler) or (arc_id == 'all'):
            ### if (arc_id == handler): ### and (handlers[handler].api_required):
                #res.append(handlers[handler].push(str(URI), p_args))
                #push_proxy( handlers[handler], str(URI), p_args, res_uris_idx)
                threads.append(Thread(target=push_proxy, args=(handlers[handler],str(URI), p_args, res_uris_idx,)))
                ### elif (arc_id == handler):
                    ### res.append(handlers[handler].push(str(URI)))

        for th in threads:
            th.start()
        for th in threads:
            th.join()

        res = res_uris[res_uris_idx]
        del res_uris[res_uris_idx]
        return res
    except:
        del res_uris[res_uris_idx]
        pass
    return ["bad request"]


def start(port=SERVER_PORT, host=SERVER_IP):
    global SERVER_PORT
    global SERVER_IP
    SERVER_PORT = port
    SERVER_IP = host
    app.run(
        host=host,
        port=port,
        threaded=True,
        debug=True,
        use_reloader=False)


def load_handlers():
    global handlers
    handlers = {}
    # add the path of the handlers to the system so they can be imported
    sys.path.append(str(PATH_HANDLER))

    # create a list of handlers.
    for file in PATH_HANDLER.glob('*_handler.py'):
        name = file.stem
        prefix = name.replace('_handler', '')
        mod = importlib.import_module(name)
        mod_class = getattr(mod, prefix.upper() + '_handler')
        # finally an object is created
        handlers[prefix] = mod_class()
    # exclude all disabled archives

    for handler in list(handlers): # handlers.keys():
        if not handlers[handler].enabled:
            del handlers[handler]


def args_parser():
    global SERVER_PORT
    global SERVER_IP
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

    parser = MyParser()

    # arc_handler = 0
    for handler in handlers:
        # add archives identifiers to the list of options
        # arc_handler += 1
        if handler == 'warc':
            parser.add_argument('--' + handler, nargs='?', 
                            help=handlers[handler].name)
        else:
            parser.add_argument('--' + handler, action='store_true', default=False,
                            help='Use ' + handlers[handler].name)
        if (handlers[handler].api_required):
            parser.add_argument(
                '--' +
                handler +
                '_api_key',
                nargs='?',
                help='An API KEY is required by ' +
                handlers[handler].name)

    parser.add_argument(
        '-v',
        '--version',
        help='Report the version of archivenow',
        action='version',
        version='ArchiveNow ' +
        archiveNowVersion)

    if len(handlers) > 0:
        parser.add_argument('--all', action='store_true', default=False,
                            help='Use all possible archives ')

        parser.add_argument('--server', action='store_true', default=False,
                            help='Run archiveNow as a Web Service ')

        parser.add_argument('URI', nargs='?', help='URI of a web resource')

        parser.add_argument('--host', nargs='?', help='A server address')

        if 'warc' in handlers.keys():
            parser.add_argument('--agent', nargs='?', help='Use "wget" or "squidwarc" for WARC generation')

        parser.add_argument(
            '--port',
            nargs='?',
            help='A port number to run a Web Service')

        args = parser.parse_args()
    else:
        print ('\n Error: No enabled archive handler found\n')
        sys.exit(0)

    arc_opt = 0
    # start the server
    if getattr(args, 'server'):
        if getattr(args, 'port'):
            SERVER_PORT = int(args.port)
        if getattr(args, 'host'):
            SERVER_IP = str(args.host)

        start(port=SERVER_PORT, host=SERVER_IP)

    else:
        if not getattr(args, 'URI'):
            print (parser.error('too few arguments'))
        res = []

        # get the args passed to push function like API KEY if provided
        PUSH_ARGS = {}
        for handler in handlers:
            if (handlers[handler].api_required):
                if getattr(args, handler + '_api_key'):
                    PUSH_ARGS[
                        handler +
                        '_api_key'] = getattr(
                        args,
                        handler +
                        '_api_key')
                else:
                    if getattr(args, handler):
                        print (
                            parser.error(
                                'An API Key is required by ' +
                                handlers[handler].name))
            orginal_warc_value = getattr(args, 'warc')
            if handler == 'warc':
                PUSH_ARGS['warc'] = getattr(args, 'warc')
                if PUSH_ARGS['warc'] == None:
                    valid_chars = "-_.()/ %s%s" % (string.ascii_letters, string.digits)
                    PUSH_ARGS['warc'] = ''.join(c for c in str(args.URI).strip() if c in valid_chars)
                    PUSH_ARGS['warc'] = PUSH_ARGS['warc'].replace(' ','_').replace('/','_').replace('__','_') # I don't like spaces in filenames.
                    PUSH_ARGS['warc'] = PUSH_ARGS['warc']+'_'+str(uuid.uuid4())[:8]
                if PUSH_ARGS['warc'][-1] == '_':
                    PUSH_ARGS['warc'] = PUSH_ARGS['warc'][:-1]
                agent = 'wget'
                tmp_agent = getattr(args, 'agent')
                if tmp_agent == 'squidwarc':
                    agent = tmp_agent
                PUSH_ARGS['agent'] = agent

        # sys.exit(0)

        # push to all possible archives
        if getattr(args, 'all'):
            arc_opt = 1
            res = push(str(args.URI).strip(), 'all', PUSH_ARGS)
        else:
            # push to the chosen archives
            for handler in handlers:
                if getattr(args, handler):
                    arc_opt += 1
                    for i in push(str(args.URI).strip(), handler, PUSH_ARGS):
                        res.append(i)
            # push to the defult archive
            if (len(handlers) > 0) and (arc_opt == 0):
                # set the default; it ia by default or the first archive in the
                # list if not found
                if 'ia' in handlers:
                    res = push(str(args.URI).strip(), 'ia', PUSH_ARGS)
                else:
                    res = push(str(args.URI).strip(),
                               handlers.keys()[0], PUSH_ARGS)
                # print (parser.printm())
            # else:
        # for rs in res:
        #     print (rs)

load_handlers()

if __name__ == '__main__':
    args_parser()
