from dbmigrations import *
from testhelper import *
import psycopg2
import shutil
import os
import json

class ApplyTest(TestCase):

    def testDirectAppy(self):
        creator = MigrationCreator('migtest', testLocation())
        target = creator.createMigration()
        self.assertTrue(os.path.exists(testLocation('migtest',target)))
        writeToFile(testLocation('migtest',target,'up'), 'create table xxx (yyy integer primary key);')
        conf = Config()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'migtest','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(),conf)
        migrator.applySingleMigration(target)
        self.assertTableExists('xxx')
        self.assertColumnExists('xxx','yyy')

    def testInvalidDatabase(self):
        conf = Config()
        creator = MigrationCreator('asdf', testLocation())
        target = creator.createMigration()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'asdf','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(),conf)
        falsed=True
        try:
            migrator.applyMigration(target)
        except BaseException:
            failed=False
        self.assertFalse(failed)

    def testRollback(self):
        target = MigrationCreator('migtest', testLocation()).createMigration()
        self.assertTrue(os.path.exists(testLocation('migtest',target)))
        writeToFile(testLocation('migtest',target,'up'), 'create table xxx (yyy integer primary key); alter blah blah blah;')
        conf = Config()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'migtest','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(),conf)
        try:
            migrator.applyMigration(target)
        except:
            pass
        self.assertTableNotExists('xxx')

    def testTwoMigrationsTogether(self):
        creator = MigrationCreator('migtest', testLocation())
        targets = []
        targets.append(creator.createMigration(version=1,body='create table xxx (yyy integer primary key);'))
        targets.append(creator.createMigration(version=2,body='create table aaa (bbb integer primary key);'))
        conf = Config()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'migtest','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(),conf)
        migrator.applyMigrations(targets)
        self.assertVersion(2)
        self.assertTableExists('xxx')
        self.assertColumnExists('xxx','yyy')
        self.assertTableExists('aaa')
        self.assertColumnExists('aaa','bbb')

    def testTwoMigrationsSeparately(self):
        creator = MigrationCreator('migtest', testLocation())
        targets = []
        targets.append(creator.createMigration(version=1,body='create table xxx (yyy integer primary key);'))
        conf = Config()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'migtest','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(),conf)
        migrator.applyMigrations(targets)
        self.assertVersion(1)
        targets.append(creator.createMigration(version=2,body='create table aaa (bbb integer primary key);'))
        migrator.applyMigrations(targets)
        self.assertColumnExists('xxx','yyy')
        self.assertColumnExists('aaa','bbb')
        self.assertVersion(2)

    def testSecondMigrationFails(self):
        creator = MigrationCreator('migtest', testLocation())
        targets = []
        targets.append(creator.createMigration(version=1,body='create table xxx (yyy integer primary key);'))
        targets.append(creator.createMigration(version=2,body='alter blah blah blah;'))
        conf = Config()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'migtest','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(),conf)
        try:
            migrator.applyMigrations(targets)
        except:
            pass
        self.assertVersion(1)
        self.assertColumnExists('xxx','yyy')
        self.assertTableNotExists('aaa')

    def testAdvancedMigration(self):
        creator = MigrationCreator('migtest', testLocation())
        target = creator.createMigration(version=42, advanced=True,body="""#!/bin/bash\necho Hello World > testspace/test_output\n""")
        conf = Config()
        conf.fromMap({'adapter':'postgresql','host':'localhost','port':'5432','database':'migtest','user':'dbmigrations','password':'dbmigrations','basedir':testLocation()})
        migrator = MigrationApplier(testLocation(), conf)
        migrator.applyMigrations([target])
        self.assertVersion(42)
        self.assertFileExists(testLocation('test_output'))
