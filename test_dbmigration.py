#!/usr/bin/env python

import unittest
from dbmigration import DbMigrator, ConfigFile
from currtime import getDatestampFromTimestamp
import shutil
import os
import json

testLocation = "testspace"
testDb = "testDb"
testPass = 'abcdef'
sampleConfigBody = {'hostname':'blergh','port':42,'database':testDb,'password':testPass,'user':'xxx'}

def deleteIfExists(location):
    if(os.path.exists(location)):
        shutil.rmtree(location)

class CreateTest(unittest.TestCase):

    def setUp(self):
        os.mkdir(testLocation)

    def tearDown(self):
        deleteIfExists(testLocation)

    def testSpaceExists(self):
        self.assertTrue(os.path.exists(testLocation))

    def testCreateMigration(self):
        migrator = DbMigrator(testDb)
        migrator.setBaseDir(testLocation)
        target = migrator.createMigration()
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.exists(target+"up"))

    def testCreateSpecificMigration(self):
        migrator = DbMigrator(testDb)
        migrator.setBaseDir(testLocation)
        target = migrator.createMigration('abcdef')
        self.assertEquals('testspace/testDb/abcdef/', target)

    def testCreateMigrationWithBody(self):
        migrator = DbMigrator(testDb)
        migrator.setBaseDir(testLocation)
        target = migrator.createMigration()
        f = open(target+"/up", 'r')
        line = f.readline()
        f.close()
        self.assertEquals("-- Sample Up migration file.\n", line)

class CurrtimeTest(unittest.TestCase):
    def testUtcTimestampsWork(self):
        datestamp = getDatestampFromTimestamp(1351066312)
        actual = "20121024081152"
        self.assertEquals(actual, datestamp)

class ConfigFileReaderTest(unittest.TestCase):

    def createSampleConfig(self, filename):
        f = open(filename, 'w')
        f.write(json.dumps(sampleConfigBody))
        f.close()

    def setUp(self):
        os.mkdir(testLocation)

    def tearDown(self):
        deleteIfExists(testLocation)

    def testCreatesConfigFile(self):
        conf = testLocation+"/config"
        self.createSampleConfig(conf)
        self.assertTrue(os.path.exists(conf))

    def testReadsFromFile(self):
        conf = testLocation+"/config"
        self.createSampleConfig(conf)
        reader = ConfigFile()
        reader.initializeFromFile(conf)
        self.assertEquals("blergh", reader.getHostname())
        self.assertEquals(42, reader.getPort())
        self.assertEquals("xxx", reader.getUser())
        self.assertEquals(testPass, reader.getPassword())
        self.assertEquals(testDb, reader.getDatabase())

if __name__=="__main__":
    unittest.main()