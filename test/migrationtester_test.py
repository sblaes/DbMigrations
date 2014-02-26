import os, stat
from testhelper import TestCase, locationInTestspace, testConfig, writeToFile, readFromFile
from fakedatabaseplugin import FakeDatabasePlugin
from dbmigrations import MigrationTester, Config, MigrationCreator, MigrationTestFailure


def chmod_x(name):
    "chmod +x name"
    os.chmod(name, os.stat(name).st_mode | stat.S_IEXEC)


class MigrationTesterTest(TestCase):
    def testRunsSimpleTest(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(body="""create table xxx (yyy integer primary key);""")
        writeToFile(locationInTestspace('migration_test', str(target), 'test'), """#!/bin/bash\necho Hello World > testspace/testRunsSimpleTest_output\nexit 0\n""")
        chmod_x(locationInTestspace('migration_test', str(target), 'test'))
        conf = Config()
        conf.fromMap(testConfig)
        tester = MigrationTester(locationInTestspace(), conf)
        tester.plugin = FakeDatabasePlugin(self)
        tester.applyMigrations([target])
        tester.plugin.assertCurrentVersion(target)
        tester.plugin.assertCommandWasExecuted('create table xxx (yyy integer primary key);')
        output = readFromFile(locationInTestspace('testRunsSimpleTest_output'))
        self.assertEquals('Hello World\n', output)

    def testRunsFailingTest(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(body="""create table xxx (yyy integer primary key);""")
        writeToFile(locationInTestspace('migration_test', str(target), 'test'), """#!/bin/bash\nexit 1\n""")
        chmod_x(locationInTestspace('migration_test', str(target), 'test'))
        conf = Config()
        conf.fromMap(testConfig)
        tester = MigrationTester(locationInTestspace(), conf)
        tester.plugin = FakeDatabasePlugin(self)
        with self.assertRaises(MigrationTestFailure):
            tester.applyMigrations([target])

    def testRunsTestFixture(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(body="""create table xxx (yyy integer primary key);""")
        writeToFile(locationInTestspace('migration_test', str(target), 'fixture'), """#!/bin/bash\necho Hello World > testspace/testRunsTestFixture_output\nexit 0\n""")
        chmod_x(locationInTestspace('migration_test', str(target), 'fixture'))
        writeToFile(locationInTestspace('migration_test', str(target), 'test'), """#!/bin/bash\nexit 0\n""")
        chmod_x(locationInTestspace('migration_test', str(target), 'test'))
        conf = Config()
        conf.fromMap(testConfig)
        tester = MigrationTester(locationInTestspace(), conf)
        tester.plugin = FakeDatabasePlugin(self)
        tester.applyMigrations([target])
        tester.plugin.assertCurrentVersion(target)
        tester.plugin.assertCommandWasExecuted('create table xxx (yyy integer primary key);')
        output = readFromFile(locationInTestspace('testRunsTestFixture_output'))
        self.assertEquals('Hello World\n', output)
