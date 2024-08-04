###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 08/11/2019.
###
from openpyweb.App import App
from openpyweb.Driver.DB.Table import  Table


class Schema(App):

    def __getattr__(self, item):
        return item


    def __init__(self):
        return None

    def table(self, table):
        self.DB()
        return Table(table)

    def raw(self, string):
        return string

    def query(self, raw):
        return self.DB().query(raw)
