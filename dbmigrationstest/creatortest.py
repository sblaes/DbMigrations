#!/usr/bin/env

import os
from dbmigrations import *
from testhelper import *

class CreateTest(TestCase):

    def setUp(self):
        create(testLocation())

    def tearDown(self):
        delete(testLocation())

    def testSpaceExists(self):
        self.assertTrue(os.path.exists(testLocation()))

    def testCreateMigration(self):
        migrator = MigrationCreator("zyxw", testLocation())
        target = migrator.createMigration()
        self.assertTrue(os.path.exists(target))
        self.assertTrue(os.path.exists(target+"up"))

    def testCreateSpecificMigration(self):
        migrator = MigrationCreator("zyxw", testLocation())
        target = migrator.createMigration('abcdef')
        self.assertEquals('testspace//zyxw/abcdef/', target)

    def testCreateMigrationWithBody(self):
        migrator = MigrationCreator("zyxw", testLocation())
        target = migrator.createMigration()
        f = open(target+"/up", 'r')
        line = f.readline()
        f.close()
        self.assertEquals("-- Sample Up migration file.\n", line)
