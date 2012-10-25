#!/usr/bin/env python

import json
import os
import shutil
import unittest

testSpace = "testspace"
testDb = "migtest"
testPass = 'abcdef'
sampleConfigBody = {'hostname':'blergh','port':42,'database':'zyxw','password':'abcdef','user':'xxx','adapter':'yyy'}
sampleConfigFile = testSpace+"/config"
actualConfigBody = {'hostname':'localhost','port':5432,'database':testDb,'password':testPass,'user':'dbmigrations','adapter':'postgresql'}

def testLocation(*filenames):
    return testSpace+"/"+("/".join(filenames))

def createSampleConfig():
    writeToFile(sampleConfigFile, json.dumps(sampleConfigBody))
    return sampleConfigFile

def createActualConfig():
    writeToFile(sampleConfigFile, json.dumps(actualConfigBody))
    return sampleConfigFile

def delete(location):
    if(os.path.exists(location)):
        shutil.rmtree(location)

def create(location):
    if(not(os.path.exists(location))):
        os.mkdir(location)

def writeToFile(filename, body):
    f = open(filename, 'w')
    f.write(body)
    f.close()

class TestCase(unittest.TestCase):
    def setUp(self):
        create(testLocation())

    def tearDown(self):
        delete(testLocation())