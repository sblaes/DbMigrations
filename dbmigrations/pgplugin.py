#!/usr/bin/env python

import psycopg2
from dbplugin import DbPlugin

VERSION_TABLE = "__mig_version__"

class PgPlugin(DbPlugin):
    def __init__(self, config):
        self.options = config
        self.conn = None
        self.cur = None
        self.open = False

    def openSession(self):
        if(self.options['password'] == None):
            self.conn = psycopg2.connect(database=self.options['database'], host=self.options['host'],
                port=self.options['port'], user=self.options['user'])
        else:
            self.conn = psycopg2.connect(database=self.options['database'], host=self.options['host'],
                port=self.options['port'], user=self.options['user'], password=self.options['password'])

    def openTransaction(self):
        if(self.conn == None):
            raise RuntimeError("Cannot open transaction without open connection.")
        self.cur = self.conn.cursor()
        self.open = True
        self.execute('SET statement_timeout TO 0;')

    def commitTransaction(self):
        self.open = False
        self.conn.commit()

    def rollbackTransaction(self):
        self.open = False
        self.conn.rollback()

    def closeSession(self):
        self.conn.close()

    def isOpen(self):
        return self.open

    def execute(self, stuff):
        if(not(self.open)):
            raise RuntimeError("Cannot execute statement without open transaction.")
        return self.cur.execute(stuff)

    def getLatestVersion(self):
        wasOpen = self.isOpen()
        if(not(self.isOpen())):
            self.openTransaction()
        try:
            self.createVersionTable()
            self.cur.execute("select max(version) from " + VERSION_TABLE)
            result = self.cur.fetchone()
            if(result == None):
                return ''
            else:
                return result[0]
        finally:
            if(not(wasOpen)):
                self.commitTransaction()

    def updateVersion(self, version):
        wasOpen = self.isOpen()
        if(not(self.isOpen())):
            self.openTransaction()
        try:
            self.createVersionTable()
            self.cur.execute("select * from " + VERSION_TABLE)
            if(self.cur.fetchone() != None):
                self.cur.execute("update " + VERSION_TABLE + " set version=%s", (version,))
            else:
                self.cur.execute("insert into " + VERSION_TABLE + " values (%s,'')", (version,))
        finally:
            if(not(wasOpen)):
                self.commitTransaction()

    def createVersionTable(self):
        self.cur.execute('select table_name from information_schema.tables where table_name = %s', (VERSION_TABLE,))
        if(self.cur.fetchone() == None):
            self.cur.execute('create table ' + VERSION_TABLE + ' (version varchar(255) primary key, status varchar(255))')
