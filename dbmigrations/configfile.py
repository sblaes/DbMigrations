#!/usr/bin/env python

import json

class ConfigFile:

    def initializeFromOptions(self, options):
        if(options["hostname"] != None):
            self.hostname = options["hostname"]
        if(options["port"] != None):
            self.port = options["port"]
        if(options["database"] != None):
            self.database = options["database"]
        if(options["user"] != None):
            self.user = options["user"]
        if(options["adapter"] != None):
            self.adapter = options["adapter"]

    def initializeFromEnv(self, env):
        if('MIG_HOST' in env):
            self.hostname = env["hostname"]
        if('MIG_PORT' in env):
            self.port = env['MIG_PORT']
        if('MIG_DB' in env):
            self.database = env['MIG_DB']
        if('MIG_USER' in env):
            self.user = env['MIG_USER']
        if('MIG_PASS' in env):
            self.password = env['MIG_PASS']
        if(options["MIG_ADAPTER"] != None):
            self.adapter = options["MIG_ADAPTER"]

    def initializeFromFile(self, file):
        f = open(file, 'r')
        s = f.read()
        f.close()
        obj = json.loads(s)
        self.hostname = obj["hostname"]
        self.port = obj["port"]
        self.database = obj["database"]
        self.password = obj["password"]
        self.user = obj["user"]
        self.adapter = obj["adapter"]

    def initialize(self, commandLineOptions, environment, configFile):
        if(commandLineOptions != None):
            initializeFromOptions(commandLineOptions)
        if(environment != None):
            initializeFromEnv(environment)
        if(configFile != None):
            initializeFromFile(configFile)

    def getHostname(self):
        return self.hostname

    def getPort(self):
        return self.port

    def getDatabase(self):
        return self.database

    def getPassword(self):
        return self.password

    def getUser(self):
        return self.user

    def getAdapter(self):
        if(self.adapter != None):
            return self.adapter
        return 'postgresql'

    def saveToFile(self, filename):
        obj = {"hostname":self.hostname,"port":self.port,"database":self.database,"password":self.password,"user":self.user}
        f = open(filename, 'w')
        f.write(json.dumps(obj,indent=4))
        f.close()