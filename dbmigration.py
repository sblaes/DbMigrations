#!/usr/bin/env python

import psycopg2
import currtime
import os
import sys
from optparse import OptionParser, OptionGroup
import json

class DbMigrator:
    def __init__(self, dbName):
        self.basedir = "."
        self.dbName = dbName

    def setBaseDir(self, newBaseDir):
        self.basedir = newBaseDir

    def createFolder(self, filename):
        if(not(os.path.exists(filename))):
            os.mkdir(filename)

    def createFile(self, filename):
        if(not(os.path.exists(filename))):
            f = open(filename, 'w')
            f.write(self.sampleUpFile())
            f.close()

    def createMigration(self, version = None):
        if(self.dbName == None):
            raise RuntimeError("Cannot create migration for null dbName")
        name = ""
        if(version == None):
            name = self.getVersion()
        else:
            name = str(version)
        self.createFolder(self.basedir + "/" + self.dbName)
        self.createFolder(self.basedir+"/"+self.dbName+"/"+name)
        target = self.basedir+"/"+self.dbName+"/"+name + "/"
        self.createFile(target + "up")
        #self.createFile(target + "down")
        return target

    def sampleUpFile(self):
        return "-- Sample Up migration file.\n"

    def getVersion(self):
        return str(currtime.getTime())

class ConfigFile:

    def initializeFromOptions(self, options):
        self.hostname = options["hostname"]
        self.port = options["port"]
        self.database = options["database"]
        self.password = None
        self.user = options["user"]

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

    def saveToFile(self, filename):
        obj = {"hostname":self.hostname,"port":self.port,"database":self.database,"password":self.password,"user":self.user}
        f = open(filename, 'w')
        f.write(json.dumps(obj,indent=4))
        f.close()

def main():
    parser = makeOptionParser()
    (options, args) = parser.parse_args()
    options = vars(options)
    actions={"create":False,"apply":False,"write":False,"help":False}
    actionsCount = 0
    if(options.get("help")):
        actions['help'] = True
        actionsCount = actionsCount+1
    if(options.get("apply")):
        actions['apply'] = True
        actionsCount = actionsCount+1
    if(options.get("config_file")):
        actions['write'] = True
        actionsCount = actionsCount+1
    if(options.get("create")):
        actions['create'] = True
        actionsCount = actionsCount+1
    if(actionsCount > 1):
        print("Too many actions provided.")
        parser.print_help()
    elif(actionsCount == 0):
        print("No action provided.")
        parser.print_help()
    else:
        hostname = options.get("hostname")
        port = options.get("port")
        database = options.get("database")
        user = options.get("user")
        if(actions['create']):
            print("Creation hasn't been implemented.")
        if(actions['help']):
            parser.print_help()
        if(actions['apply']):
            print("Apply hasn't been implemented.")
        if(actions['write']):
            config = ConfigFile()
            config.initializeFromOptions(options)
            config.saveToFile(options["config_file"])  
            

def makeOptionParser():
    parser = OptionParser(usage="usage: %prog [action] [options]", add_help_option=False)
    action_group = OptionGroup(parser, "Actions", "Exactly one action must be provided.")
    action_group.add_option("-c","--create",action="store_true",dest="create",help="Create a migration.")
    action_group.add_option("-a","--apply",action="store_true",dest="apply",help="Apply migrations.")
    action_group.add_option("-w","--write-config",dest="config_file",help="Write configuration options to file and exit.")
    action_group.add_option("--help",action="store_true",dest="help",help="Show this help message and exit.")
    parser.add_option_group(action_group)
    connection_group = OptionGroup(parser, "Connection Options", "These options can be specified from a configuration file. Command line options override configuration files.")
    connection_group.add_option("-h","--host","--hostname",dest="hostname",help="Specify the database hostname. Default localhost.")
    connection_group.add_option("-p","--port",dest="port",help="Specify the database port. Default 5432.")
    connection_group.add_option("-U","--user",dest="user",help="Specify the database user. Required.")
    connection_group.add_option("-d","--db","--database",dest="database",help="Specify the database name. Required.")
    parser.add_option_group(connection_group)
    options_group = OptionGroup(parser, "Other Options")
    options_group.add_option("-b","--basedir",dest="basedir",help="Specify the migration base directory. The migrator will look here for the connection config file.")
    parser.add_option_group(options_group)
    return parser

if(__name__=="__main__"):
    main()