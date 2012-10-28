#!/usr/bin/env python

import psycopg2
from dbplugin import DbPlugin

class PgPlugin(DbPlugin):
    def __init__(self):
        self.options = {}
        self.conn = None
        self.cur = None

    def setOption(self, key, value):
        self.options[key] = value

    def openSession(self):
        if(self.options['password'] == None):
            self.conn = psycopg2.connect(database=self.options['database'], host=self.options['hostname'],
                port=self.options['port'], user=self.options['user'])
        else:
            self.conn = psycopg2.connect(database=self.options['database'], host=self.options['hostname'],
                port=self.options['port'], user=self.options['user'], password=self.options['password'])
        self.cur = self.conn.cursor()
        self.open = True

    def commit(self):
        self.open = False
        self.conn.commit()

    def rollback(self):
        self.open = False
        self.conn.rollback()

    def closeSession(self):
        self.open = False
        self.cur.close()
        self.conn.close()

    def isOpen(self):
        return self.open

    def execute(self, stuff):
        raise NotImplementedError("Cannot evaluate unimplemented function.")