###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###


import os
import cgi
from openpyweb.Controllers import Controllers
from openpyweb.util.Variable import Variable
from openpyweb.Version import *
from openpyweb.Log import Log


class Request(Variable):

    def __getattr__(self, item):
        return item

    def __init__(self, prform=None):
        self.Controllers = Controllers()
        self.para_vv ={}
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            self.attr = prform
        else:
            self.attr = cgi.FieldStorage()
        self.method = self.out('REQUEST_METHOD', '')

    def get(self, key=0, error=0):
        if 'GET' == self.method:
            if error == 1:
                try:
                    return self.attr
                except Exception as e:
                    return self.param()

            if key != 0:
                try:
                    if (key in self.attr):
                        if self.attr.getvalue(key) != "":
                            return self.attr.getvalue(key)
                        else:
                            return self.param(key)
                except Exception as e:
                    return self.param(key)
            else:
                try:
                    return self.attr
                except Exception as e:
                    return self.param()


    def post(self, key=0, error=0):
        if 'POST' == self.method:
            if error == 1:
                try:
                    return self.attr
                except Exception as e:
                    return None

            if key != 0:
                try:
                    if (key in self.attr):
                        if self.attr.getvalue(key) != "":
                            return self.attr.getvalue(key)
                        else:
                            return None
                except Exception as e:
                    return None
            else:
                return None

    def file(self, key=0, error=0):
        try:
            if key != 0:
                if (key in self.attr):
                    self.attr.getvalue(key)
                    return self.attr[key]
                elif error == 1:
                    return self.attr
                else:
                    return None
            else:
                return None

        except Exception as err:
            Log('').warning(err)
            return None

    def all(self):
        if None is not self.attr.keys():
            return self.attr.keys()

    def _getparamuri(self):
        _params = dict()
        uri_sp = self.out("REQUEST_URI").split('?')
        if len(uri_sp) > 1:
            for uri_s in uri_sp:
                _uri_x = str(uri_s).split('&')
                for _uri_f in _uri_x:
                    _url_e = _uri_f.split('=')
                    if len(_url_e) > 1:
                        _k, _v = _url_e[0], _url_e[1]
                        _params[str(_k)] = _v
        return _params

    def param(self, key=""):
        if len(self.Controllers._getParams()) > 0:
            self.para_vv = self.Controllers._getParams()
        else:
            self.para_vv  = self._getparamuri()
        if key == "" or key == None:
            result = self.para_vv
        else:
            result =  self.para_vv.get(key, None)
        return result
