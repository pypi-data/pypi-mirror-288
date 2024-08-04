###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###
import base64
import traceback
import cgi
import ssl
import argparse
import locale
import os
import re
import sys
import time
import json
import warnings
from openpyweb.cmd import lang
from openpyweb.Version import *
from openpyweb.util.Variable import Variable
from typing import Any, Callable, Dict, List, Pattern, Union
from openpyweb.cmd.console import (  # type: ignore
    colorize, bold, red, green, turquoise, nocolor, color_terminal
)

try:
    from http import cookies as cook
except Exception as err:
    import Cookie as cook

from socketserver import ThreadingMixIn

try:
    from BaseHTTPServer import BaseHTTPRequestHandler
except Exception as err:
    from http.server import BaseHTTPRequestHandler, HTTPServer
try:
    import socket
except Exception as err:
    from socket import socket

try:
    import http.client as htp
    from http import client
    import urllib as urllib
except Exception as err:
    import httplib as htp
    import urllib2 as urllib

try:
    import imp as im
except Exception as err:
    import importlib as im

varb = Variable()

port = 80


global response_code, mimetype
mimetype = 'text/html'
redirect_code = ["500", "400", "404", "405", "451", "301", "302", "307"]
def load_source(modname, filename):
    import types
    with open(filename, "rb") as f:
        mod = types.ModuleType(modname)
        exec(f.read(), mod.__dict__)
    return mod

def run(host="", path="", port=6060, server_pro="HTTP/1.1", ssl_ip="", ssl_port="", pr=False):
    server = HTTPServer

    path = str(path).replace("\\", "/") if path != "" else str(os.getcwd()).replace("\\", "/")

    spes = "/"
    sys.path.insert(0, os.path.dirname(__file__))
    os.chdir(path)

    class httpv(BaseHTTPRequestHandler):

        def do_GET(self):
            path_info = self.path
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': "GET",
                    'CONTENT-TYPE': self.headers['Centent-Type']
                }
            )
            if self.path == spes:
                if os.path.isfile(os.path.join(str(path),"public", "index.py")) == True:
                    vpath = os.path.join("public", "index.py")

                elif os.path.isfile(os.path.join(str(path),"public", "home.py")) == True:
                    vpath = os.path.join("public", "home.py")
                elif os.path.isfile(os.path.join(str(path),"public", "default.py")) == True:
                    vpath = os.path.join("public", "default.py")

                try:
                    App = im.load_source('App.App', os.path.join(path,vpath))
                except Exception as e:
                    App = load_source('App.App', os.path.join(path,vpath))

                self._App = App.App()
                if "." not in path_info:

                    self._App.put(method="GET", accept_lang=self.headers["Accept-Language"],
                            http_connect=self.headers["Connection"], http_user_agt=self.headers["User-Agent"],
                            http_encode=self.headers["Accept-Encoding"], path=path, host=host, port=port,
                            para=path_info, remoter_addr=self.client_address[
                                0], remoter_port=self.client_address[1],
                            script_file=os.path.join(path, vpath), server_proto=server_pro, server_ver=self.server_version,
                            protocol_ver=self.protocol_version)

                    runs_response = self._App.runs(formData=form, serverobj=self)
                    if isinstance(runs_response, tuple) == True:

                        if str(runs_response[0]).isnumeric() == True:

                            if runs_response[0] in redirect_code:
                                self.redirect(runs_response[0], runs_response[1])
                            else:
                                self.rendering(mimetype=mimetype, content=runs_response)

                        if len(runs_response) == 4:
                            self.setwriter(runs_response[1], runs_response[2], runs_response[3])
                    else:
                        self.rendering(mimetype=mimetype, content=runs_response)

            elif self.path != spes:

                if "." not in str(self.path):

                    if str(self.path) != "":
                        if os.path.isfile(os.path.join(str(path), "public", "index.py")) == True:
                            vpath = os.path.join("public","index.py")

                        elif os.path.isfile(os.path.join(str(path), "public","home.py")) == True:
                            vpath = os.path.join("public","home.py")

                        elif os.path.isfile(os.path.join(str(path),"public","default.py")) == True:

                            vpath = os.path.join("public","default.py")

                        try:
                            App = im.load_source('App.App', os.path.join(path,vpath))
                        except:
                            App = load_source('App.App', os.path.join(path,vpath))

                        self._App = App.App()
                        if "." not in path_info:


                            self._App.put(method="GET", accept_lang=self.headers["Accept-Language"],
                                        http_connect=self.headers["Connection"], http_user_agt=self.headers["User-Agent"],
                                        http_encode=self.headers["Accept-Encoding"], path=path, host=host, port=port,
                                        para=path_info, remoter_addr=self.client_address[0],
                                        remoter_port=self.client_address[1], script_file=os.path.join(
                                path, vpath), server_proto=server_pro, server_ver=self.server_version,
                                protocol_ver=self.protocol_version)

                            runs_response = self._App.runs(formData=form, serverobj=self)

                            if isinstance(runs_response, tuple) == True:

                                if str(runs_response[0]).isnumeric() == True:

                                    if runs_response[0] in redirect_code:
                                        self.redirect(runs_response[0], runs_response[1])
                                    else:
                                        self.rendering(mimetype=mimetype, content=runs_response)

                                if len(runs_response) == 4:
                                    self.setwriter(runs_response[1], runs_response[2], runs_response[3])

                            else:
                                self.rendering(mimetype=mimetype, content=runs_response)




            if self.path.endswith('favicon.ico'):
                return
            try:
                for mime in MIME_TYPES:
                    if self.path.endswith(mime['ext']):
                        self.rendering(
                            path=path, mimetype=mime['type'], mode=mime['mode'], code=200)
                    else:
                        split_path = str(self.path).split('?')
                        if split_path[0].endswith(mime['ext']):
                            self.rendering(
                            path=path, mimetype=mime['type'], mode=mime['mode'], code=200)


            except Exception as err:
                if self.path.endswith(self.path):
                    if os.path.isfile(os.path.join(str(path),"public","index.py"))== True:
                        vpath = os.path.join("public","index.py")

                    elif os.path.isfile(os.path.join(str(path),"public", "home.py")) == True:
                        vpath = os.path.join("public","home.py")

                    elif os.path.isfile(os.path.join(str(path),"public", "default.py")) == True:
                        vpath = os.path.join("public","default.py")

                    try:
                        App = im.load_source('App.App', os.path.join(path,vpath))
                    except Exception as e:
                        App = load_source('App.App', os.path.join(path,vpath))
                    self._App = App.App()
                    code = "500"
                    self._App.put(status=code)
                    _code, _url = self._App.errorP(code=code)
                    self.redirect(_code, _url)

        def do_POST(self):

            path_info = self.path

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': "POST",
                    'CONTENT-TYPE': self.headers['Content-Type']
                }
            )

            # text/plain; charset=utf-8
            if os.path.isfile(os.path.join(str(path),"public", "index.py")) == True:
                vpath = os.path.join("public","index.py")

            elif os.path.isfile(os.path.join(str(path),"public", "home.py")) == True:
                vpath = os.path.join("public", "home.py")

            else:
                vpath = os.path.join("public", "default.py")

            try:
                App = im.load_source('App.App', os.path.join(path,vpath))
            except:
                App = load_source('App.App', os.path.join(path,vpath))
            self._App = App.App()
            if "." not in path_info :


                self._App.put(method="POST", accept_lang=self.headers["Accept-Language"],
                            http_connect=self.headers["Connection"], http_user_agt=self.headers["User-Agent"],
                            http_encode=self.headers["Accept-Encoding"], path=path, host=host, port=port, para=path_info,
                            remoter_addr=self.client_address[0], remoter_port=self.client_address[1], script_file=os.path.join(path, vpath), server_proto=server_pro, server_ver=self.server_version,
                    protocol_ver=self.protocol_version)

                runs_response = self._App.runs(formData=form, serverobj=self)
                if isinstance(runs_response, tuple) == True:
                    if str(runs_response[0]).isnumeric() == True:

                        if runs_response[0] in redirect_code:
                            self.redirect(runs_response[0], runs_response[1])
                        else:
                            self.rendering(mimetype=mimetype, code=200, content=self._App.runs(formData=form, serverobj=self))
                    else:
                        if len(runs_response) == 4:
                            self.setwriter(runs_response[1], runs_response[2], runs_response[3])

                else:
                    self.rendering(mimetype=mimetype, code=200, content=self._App.runs(formData=form, serverobj=self))

        def do_HEAD(self):
            self.do_GET()

        def do_PUT(self):
            self.do_POST()

        def setwriter(self, code, content, mimetype="text/html"):
            try:
                self.send_response(int(code))
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(str(content).encode()))
            except Exception as e:
                print(f'SetWriter Error: {e}')
                pass

        def setcookie(self, code, name, cooKeys):
            self.send_response(int(code))
            self.send_header("Content-type", "text/html")
            for morsel in cooKeys.values():
                self.send_header(name, morsel.OutputString())
            #self.end_headers()

        def rendering(self, path="", mimetype="", mode='r', encoding="utf-8", content="", code=200):
            try:
                self.send_response(int(code))
                self.send_header('Content-type', mimetype)
                self.end_headers()
                if path != "":

                    f = open(path + self.path, mode)
                    readv = ""
                    if mode == "rb":
                        readv = f.read()
                    else:
                        readv = bytes(str(f.read()).encode('utf-8'))

                    self.wfile.write(readv)

                    f.close()

                elif content != "":
                    self.wfile.write(bytes(str(content).encode()))
            except Exception as e:
                print(f'Rendering Error: {e}')
                pass


        def redirect(self, code, re_url, code_re=307):
            try:
                self.send_response(int(code_re))
                self.send_header("Content-type", "")
                self.send_header('Location', "{re_url}".format(re_url=re_url))
                self.send_error(code=int(code), message=HTTP_CODE.get(code, ""))
                self.end_headers()
            except Exception as e:
                pass




    class ThreadedHTTPServer(ThreadingMixIn, server):
        """Moomins live here"""
    hostname = ssl_ip if ssl_ip != "" else host
    portnumber = int(ssl_port) if ssl_port != "" else int(port)
    vars_http = ""
    try:
        context = ssl.create_default_context()

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # print(ssock.version())
                data = json.dumps(ssock.getpeercert())
        varb.put(ssl_v="on")
        vars_http = "https://"
        # print(ssock.getpeercert())
    except Exception as err:
        try:
            cert = ssl.get_server_certificate((hostname, int(portnumber)))
            varb.put(ssl_v="on")
            vars_http = "https://"
        except Exception as err:
            varb.put(ssl_v="off")
            vars_http = "http://"

    try:
        l = host if str(port) == "8080" or str(port) == "80" else "{}:{}".format(
            host, port)
        if pr == True:

            print(
                bold(green("openpyweb development server running on " + str(vars_http) + str(l))))
        else:
            print(bold(green("openpyweb server running on " + str(vars_http) + str(l))))

        server = ThreadedHTTPServer((host, port), httpv)
        server.serve_forever()
        server.server_close()
    except Exception as err:
        print(bold(red("Something went wrong: Default port already in use")))

def terminated():
    return exit('Server Terminated')
