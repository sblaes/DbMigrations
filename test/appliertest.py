from dbmigrations import MigrationCreator, Config, MigrationApplier
from testhelper import TestCase, locationInTestspace, writeToFile, testConfig
from fakedatabaseplugin import FakeDatabasePlugin, FakeMultiPlugin
import os

class ApplyTest(TestCase):

    def testDirectAppy(self):
        command = 'create table xxx (yyy integer primary key);'
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration()
        self.assertFolderExists('migration_test', target)
        writeToFile(locationInTestspace('migration_test', target, 'up'), command)
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        migrator.applySingleMigration(target)
        migrator.plugin.assertCommandWasExecuted(command)

    def testRollback(self):
        command = 'create table xxx (yyy integer primary key); alter blah blah blah;'
        target = MigrationCreator('migration_test', locationInTestspace()).createMigration()
        self.assertFolderExists('migration_test', target)
        writeToFile(locationInTestspace('migration_test', target, 'up'), command)
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        try:
            migrator.applyMigration(target)
        except:
            pass
        migrator.plugin.assertNoCommandWasExecuted()

    def testTwoMigrationsTogether(self):
        command0 = 'create table xxx (yyy integer primary key);'
        command1 = 'create table aaa (bbb integer primary key);'
        creator = MigrationCreator('migration_test', locationInTestspace())
        targets = []
        targets.append(creator.createMigration(version=1, body=command0))
        targets.append(creator.createMigration(version=2, body=command1))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        migrator.applyMigrations(targets)
        migrator.plugin.assertCurrentVersion(2)
        migrator.plugin.assertCommandWasExecuted(command0)
        migrator.plugin.assertCommandWasExecuted(command1)

    def testTwoMigrationsSeparately(self):
        command0 = 'create table xxx (yyy integer primary key);'
        command1 = 'create table aaa (bbb integer primary key);'
        creator = MigrationCreator('migration_test', locationInTestspace())
        targets = []
        targets.append(creator.createMigration(version=1, body=command0))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        migrator.applyMigrations(targets)
        migrator.plugin.assertCurrentVersion(1)
        targets.append(creator.createMigration(version=2, body=command1))
        migrator.applyMigrations(targets)
        migrator.plugin.assertCommandWasExecuted(command0)
        migrator.plugin.assertCommandWasExecuted(command1)
        migrator.plugin.assertCurrentVersion(2)

    def testSecondMigrationFails(self):
        command0 = 'create table xxx (yyy integer primary key);'
        command1 = 'alter blah blah blah;'
        creator = MigrationCreator('migration_test', locationInTestspace())
        targets = []
        targets.append(creator.createMigration(version=1, body=command0))
        targets.append(creator.createMigration(version=2, body=command1))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self, failOn=command1)
        try:
            migrator.applyMigrations(targets)
        except:  # Error is expected
            pass
        migrator.plugin.assertCurrentVersion(1)
        migrator.plugin.assertCommandWasExecuted(command0)
        migrator.plugin.assertCommandWasNotExecuted(command1)

    def testAdvancedMigration(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(version=42, advanced=True, body="""#!/bin/bash\necho Hello World > testspace/test_output\n""")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        migrator.applyMigrations([target])
        migrator.plugin.assertCurrentVersion(42)
        self.assertFileExists('test_output')
    
    def testPipesAdvancedOutput(self):
        command = 'create table xxx (yyy integer primary key);'
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(version=42, advanced=True, body="#!/bin/bash\necho -n '"+command+"' ")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        migrator.applyMigrations([target])
        migrator.plugin.assertCurrentVersion(42)
        migrator.plugin.assertCommandWasExecuted(command)
    
    def testEmptyUpFile(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target1 = creator.createMigration(version=17, body="""select * from __mig_version__""")
        target2 = creator.createMigration(version=23, body="""""")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        self.assertRaisesRegexp(RuntimeError, "Invalid migration: Up file is empty", migrator.applyMigrations, ([target1, target2]))
        migrator.plugin.assertCurrentVersion(17)
    
    def testMissingUpFile(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target1 = creator.createMigration(version=17, body="""select * from __mig_version__""")
        target2 = creator.createMigration(version=23, body="""""")
        os.remove(locationInTestspace('migration_test',target2,'up'))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin(self)
        self.assertRaisesRegexp(RuntimeError, "Invalid migration: Up file not found", migrator.applyMigrations, ([target1, target2]))
        migrator.plugin.assertCurrentVersion(17)

    def testAppliesOutOfOrderMigrations(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target1 = creator.createMigration(version=23, body='select 1')
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeMultiPlugin(self)
        migrator.applySingleMigration(target1)
        target2 = creator.createMigration(version=17, body='select 2')
        migrator.applyMigrations([target1,target2])
        migrator.plugin.assertCurrentVersion(23)
        migrator.plugin.assertCommandWasExecuted('select 1')
        migrator.plugin.assertCommandWasExecuted('select 2')



