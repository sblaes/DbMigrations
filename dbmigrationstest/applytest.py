#!/usr/bin/env python

from dbmigrations import *
from testhelper import *
import psycopg2
import shutil
import os
import json

class ApplyTest(TestCase):

    def testDirectAppy(self):
        config = ConfigFile()
        config.initializeFromFile(createActualConfig())
        creator = MigrationCreator("zyxw", testLocation())
        target = creator.createMigration()
        self.assertTrue(os.path.exists(target))
        writeToFile(target+"/up", "create table xxx (yyy integer primary key);")
        migrator = DbMigrator(config)
        migrator.applyMigration(target)