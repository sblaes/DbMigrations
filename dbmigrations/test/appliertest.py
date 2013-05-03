from dbmigrations import MigrationCreator, Config, MigrationApplier
from testhelper import TestCase, locationInTestspace, writeToFile, testConfig
from fakedatabaseplugin import FakeDatabasePlugin
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
        migrator.plugin = FakeDatabasePlugin()
        migrator.applySingleMigration(target)
        self.assertCommandWasExecuted(migrator, command)

    def testRollback(self):
        command = 'create table xxx (yyy integer primary key); alter blah blah blah;'
        target = MigrationCreator('migration_test', locationInTestspace()).createMigration()
        self.assertFolderExists('migration_test', target)
        writeToFile(locationInTestspace('migration_test', target, 'up'), command)
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin()
        try:
            migrator.applyMigration(target)
        except:
            pass
        self.assertNoCommandWasExecuted(migrator)

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
        migrator.plugin = FakeDatabasePlugin()
        migrator.applyMigrations(targets)
        self.assertVersion(migrator, 2)
        self.assertCommandWasExecuted(migrator, command0)
        self.assertCommandWasExecuted(migrator, command1)

    def testTwoMigrationsSeparately(self):
        command0 = 'create table xxx (yyy integer primary key);'
        command1 = 'create table aaa (bbb integer primary key);'
        creator = MigrationCreator('migration_test', locationInTestspace())
        targets = []
        targets.append(creator.createMigration(version=1, body=command0))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin()
        migrator.applyMigrations(targets)
        self.assertVersion(migrator, 1)
        targets.append(creator.createMigration(version=2, body=command1))
        migrator.applyMigrations(targets)
        self.assertCommandWasExecuted(migrator, command0)
        self.assertCommandWasExecuted(migrator, command1)
        self.assertVersion(migrator, 2)

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
        migrator.plugin = FakeDatabasePlugin(failOn=command1)
        try:
            migrator.applyMigrations(targets)
        except:  # Error is expected
            pass
        self.assertVersion(migrator, 1)
        self.assertCommandWasExecuted(migrator, command0)
        self.assertCommandWasNotExecuted(migrator, command1)

    def testAdvancedMigration(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(version=42, advanced=True, body="""#!/bin/bash\necho Hello World > testspace/test_output\n""")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin()
        migrator.applyMigrations([target])
        self.assertVersion(migrator, 42)
        self.assertFileExists('test_output')
    
    def testPipesAdvancedOutput(self):
        command = 'create table xxx (yyy integer primary key);'
        creator = MigrationCreator('migration_test', locationInTestspace())
        target = creator.createMigration(version=42, advanced=True, body="#!/bin/bash\necho -n '"+command+"' ")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin()
        migrator.applyMigrations([target])
        self.assertVersion(migrator, 42)
        self.assertCommandWasExecuted(migrator, command)
    
    def testEmptyUpFile(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target1 = creator.createMigration(version=17, body="""select * from __mig_version__""")
        target2 = creator.createMigration(version=23, body="""""")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin()
        self.assertRaisesRegexp(RuntimeError, "Invalid migration: Up file is empty", migrator.applyMigrations, ([target1, target2]))
        self.assertVersion(migrator, 17)
    
    def testMissingUpFile(self):
        creator = MigrationCreator('migration_test', locationInTestspace())
        target1 = creator.createMigration(version=17, body="""select * from __mig_version__""")
        target2 = creator.createMigration(version=23, body="""""")
        os.remove(locationInTestspace('migration_test',target2,'up'))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(locationInTestspace(), conf)
        migrator.plugin = FakeDatabasePlugin()
        self.assertRaisesRegexp(RuntimeError, "Invalid migration: Up file not found", migrator.applyMigrations, ([target1, target2]))
        self.assertVersion(migrator, 17)

    def assertCommandWasExecuted(self, applier, command):
        plugin = applier.plugin
        self.assertTrue(plugin.commandWasExecuted(command), "Command '" + command + "' was not executed")

    def assertNoCommandWasExecuted(self, applier):
        plugin = applier.plugin
        self.assertEqual(0, len(plugin.committedCommands), 'Commands were executed when they shouldn\'t have.')

    def assertCommandWasNotExecuted(self, applier, command):
        plugin = applier.plugin
        self.assertFalse(plugin.commandWasExecuted(command), "Command '" + command + "' was executed")

    def assertVersion(self, applier, version):
        plugin = applier.plugin
        self.assertEqual(version, plugin.currentVersion, 'Expected version: '+str(version)+' but actual: '+str(plugin.currentVersion))