#!/usr/bin/env python

from pgplugin import PgPlugin
import currtime
import os
import sys
from optparse import OptionParser, OptionGroup
import json
import time

class DbMigrator:
    def __init__(self, config):
        self.basedir = "."
        self.config = config
        self.plugin = None

    def setBaseDir(self, newBaseDir):
        self.basedir = newBaseDir

    def applyMigration(self, migVersion):
        self.initializePlugin()
        self.plugin.openSession()
        self.plugin.closeSession()

    def applySingleMigration(self, migVersion):
        try:
            if(self.config.getAdapter() == 'postgresql'):
                applySinglePostgresql(self, migVersion)
            else:
                raise RuntimeError("Invalid database adapter: "+self.config.getAdapter())
        except KeyboardInterrupt as e:
            print("Keyboard Interrupt in migration "+migVersion+". Closing session.")
            self.plugin.closeSession()
            raise e
        except Exception as e:
            print("Exception in migration "+migVersion+". Closing session.")
            self.plugin.closeSession()
            raise e

    def applySinglePostgresql(self, migVersion):
        self.plugin.checkout()
        f = open(migVersion+'/up','r')
        stuff = f.read()
        f.close()
        print("Applying migration "+migVersion)
        self.plugin.execute(stuff)
        self.plugin.commit()
        print("Migration "+migVersion+" applied successfully.")

    def initializePlugin(self):
        self.plugin = None
        adapter = self.config.getAdapter()
        if(adapter == 'postgresql'):
            self.plugin = PgPlugin()
            self.plugin.setOption('hostname', self.config.getHostname())
            self.plugin.setOption('port', self.config.getPort())
            self.plugin.setOption('database', self.config.getDatabase())
            self.plugin.setOption('user', self.config.getUser())
            self.plugin.setOption('password', self.config.getPassword())
        else:
            raise RuntimeError("Invalid database adapter: "+adapter)
        return adapter