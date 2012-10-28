#!/usr/bin/env python

from dbmigrations import *
from testhelper import *
import psycopg2
import shutil
import os
import json

class ApplyTest(TestCase):

    def testDirectAppy(self):
        creator = MigrationCreator("migtest", testLocation())
        target = creator.createMigration()
        self.assertTrue(os.path.exists(target))
        writeToFile(target+"/up", "create table xxx (yyy integer primary key);")
        migrator = MigrationApplier('postgresql','localhost', '5432', "migtest",'dbmigrations', None, testLocation())
        migrator.applyMigration(target)