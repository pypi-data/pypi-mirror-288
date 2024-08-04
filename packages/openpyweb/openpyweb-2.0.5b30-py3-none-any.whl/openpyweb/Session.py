###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###


import os
import datetime, time
import sys
import ast
from openpyweb.Version import *
from openpyweb.Log import Log
from openpyweb.util.Variable import Variable
from openpyweb.util.Crypt import Crypt


try:
    from http import cookies as cook
except Exception as err:
    import Cookie as cook


class Session(Variable):
    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None

    def __init__(self, prsee=None):
        self.result = ""
        self.prsee = prsee #from the server
        self.s_string = "HTTP_COOKIE"
        self.session_list = []
        self._commit = []

        return None

    def has(self, key=""):
        bool_v = False

        if self.get(key) != "" and self.get(key) != None:

            bool_v = True
        else:
            bool_v = False

        return bool_v

    def set(self, key="", value=None, res_code=302, duration=3600, url="", path="/",  samesite="", httponly=False, secure=False, max_age="", encrypt = False):
        _value = Crypt._encode(value) if encrypt == True else value
        return self._set(key, _value, res_code, duration, url, path, samesite, httponly, secure, max_age)


    def _set(self, key="", value=None, res_code=302, duration=3600, url="", path="/", samesite="", httponly=False, secure=False, max_age="")->bool:



        url_v = self.out("HTTP_HOST") + str(":") + str(self.out("SERVER_PORT", '')) if self.out("HTTP_HOST") == "localhost" or self.out("HTTP_HOST") == "127.0.0.1" else self.out("HTTP_HOST")
        url = url if url != "" else url_v
        expires = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=duration)
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            cooKeys = cook.SimpleCookie()
        else:
            cooKeys = cook.SimpleCookie(self.out(self.s_string))
        cooKeys["{key}".format(key=key)] = value
        #cooKeys["{key}".format(key=key)]["domain"] = url
        cooKeys["{key}".format(key=key)]["path"] = path
        cooKeys["{key}".format(key=key)]['samesite'] = samesite
        cooKeys["{key}".format(key=key)]["httponly"] = httponly
        cooKeys["{key}".format(key=key)]["secure"] = secure
        cooKeys["{key}".format(key=key)]["max-age"] = max_age
        cooKeys["{key}".format(key=key)]["expires"] = expires.strftime('%a, %d %b %Y %H:%M:%S')
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            if self.prsee !=None:
                self.prsee.setcookie(307, "Set-Cookie", cooKeys)
        else:
            print(cooKeys[str(key)])
        time.sleep(0.5)
        return True

    def get(self, key=""):
        OsEnviron = None
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            try:
                OsEnviron = self.prsee.headers.get('Cookie')
            except Exception as e:
                pass

        else:
            OsEnviron = self.out(self.s_string)

        if OsEnviron != None:
            cooKeys = cook.SimpleCookie(OsEnviron)
            cooKeys.load(OsEnviron)
            if key in cooKeys:
                if cooKeys[key].value != None or cooKeys[key].value != "":

                    if Crypt._isbase(cooKeys[key].value) == True:
                        try:
                            return ast.literal_eval(Crypt._decode(cooKeys[key].value))
                        except Exception as err:
                            return Crypt._decode(cooKeys[key].value)
                    else:
                        return cooKeys[key].value
                else:
                    return None
            else:
                return None
        else:
            return None

    def destroy(self, key="", path= "/"):
        bool_v = False
        OsEnviron = None
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            try:
                OsEnviron = self.prsee.headers.get('Cookie')
            except Exception as e:
                pass

        else:
            OsEnviron = self.out(self.s_string)

        if OsEnviron != None:
            cooKeys = cook.SimpleCookie(OsEnviron)
            cooKeys.load(OsEnviron)
            if PYVERSION_MA >= 3:

                cookv = cooKeys.items()
            else:
                cookv = cooKeys.iteritems()

            if cookv != None or cookv != "":
                if key !="":

                    if self.get(key) != "":
                        duration = 3600 * 30 * 1000
                        self._set(key=key, duration=-duration, path=path)
                        return True

                else:
                    bool_vx = False
                    for key, v in cookv:
                        if self.get(key) != "":
                            duration = 3600 * 33 * 100
                            self._set(key=key, duration=-duration)
                            bool_vx = True
                    return bool_vx

        return False

    def _update(self, session_string):
        dict_session = dict({self.s_string: session_string})
        try:
            self.update(dict_session)
            return True
        except Exception as e:
            return False

    def _reset(self, session_dict=dict()):

        session_list = []
        if PYVERSION_MA >= 3:
            session_dict_l = session_dict.items()
        else:
            session_dict_l = session_dict.iteritems()

        for k, v in session_dict_l:
            session_list.append("{k}={v}".format(k=k, v=v))

        return self._update(";".join(session_list))
