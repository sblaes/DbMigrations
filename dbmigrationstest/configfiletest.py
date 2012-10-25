#!/usr/bin/env python

from testhelper import *
from dbmigrations import ConfigFile

class ConfigFileTest(TestCase):

    def testCreatesConfigFile(self):
        conf = createSampleConfig()
        self.assertTrue(os.path.exists(conf))

    def testReadsFromFile(self):
        conf = createSampleConfig()
        reader = ConfigFile()
        reader.initializeFromFile(conf)
        self.assertEquals("blergh", reader.getHostname())
        self.assertEquals(42, reader.getPort())
        self.assertEquals("xxx", reader.getUser())
        self.assertEquals("abcdef", reader.getPassword())
        self.assertEquals("zyxw", reader.getDatabase())
        self.assertEquals("yyy", reader.getAdapter())