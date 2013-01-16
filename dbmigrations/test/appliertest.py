from dbmigrations import MigrationCreator, Config, MigrationApplier
from testhelper import TestCase, testLocation, writeToFile, testConfig
import os

class ApplyTest(TestCase):

    def testDirectAppy(self):
        creator = MigrationCreator('migration_test', testLocation())
        target = creator.createMigration()
        self.assertFolderExists('migration_test', target)
        writeToFile(testLocation('migration_test', target, 'up'), 'create table xxx (yyy integer primary key);')
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        migrator.applySingleMigration(target)
        self.assertTableExists('xxx')
        self.assertColumnExists('xxx', 'yyy')

    def testInvalidDatabase(self):
        conf = Config()
        creator = MigrationCreator('asdf', testLocation())
        target = creator.createMigration()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        failed = True
        try:
            migrator.applyMigration(target)
        except BaseException:
            failed = False
        self.assertFalse(failed)

    def testRollback(self):
        target = MigrationCreator('migration_test', testLocation()).createMigration()
        self.assertFolderExists('migration_test', target)
        writeToFile(testLocation('migration_test', target, 'up'), 'create table xxx (yyy integer primary key); alter blah blah blah;')
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        try:
            migrator.applyMigration(target)
        except:
            pass
        self.assertTableNotExists('xxx')

    def testTwoMigrationsTogether(self):
        creator = MigrationCreator('migration_test', testLocation())
        targets = []
        targets.append(creator.createMigration(version=1, body='create table xxx (yyy integer primary key);'))
        targets.append(creator.createMigration(version=2, body='create table aaa (bbb integer primary key);'))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        migrator.applyMigrations(targets)
        self.assertVersion(2)
        self.assertTableExists('xxx')
        self.assertColumnExists('xxx', 'yyy')
        self.assertTableExists('aaa')
        self.assertColumnExists('aaa', 'bbb')

    def testTwoMigrationsSeparately(self):
        creator = MigrationCreator('migration_test', testLocation())
        targets = []
        targets.append(creator.createMigration(version=1, body='create table xxx (yyy integer primary key);'))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        migrator.applyMigrations(targets)
        self.assertVersion(1)
        targets.append(creator.createMigration(version=2, body='create table aaa (bbb integer primary key);'))
        migrator.applyMigrations(targets)
        self.assertColumnExists('xxx', 'yyy')
        self.assertColumnExists('aaa', 'bbb')
        self.assertVersion(2)

    def testSecondMigrationFails(self):
        creator = MigrationCreator('migration_test', testLocation())
        targets = []
        targets.append(creator.createMigration(version=1, body='create table xxx (yyy integer primary key);'))
        targets.append(creator.createMigration(version=2, body='alter blah blah blah;'))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        try:
            migrator.applyMigrations(targets)
        except:  # Error is expected
            pass
        self.assertVersion(1)
        self.assertColumnExists('xxx', 'yyy')
        self.assertTableNotExists('aaa')

    def testAdvancedMigration(self):
        creator = MigrationCreator('migration_test', testLocation())
        target = creator.createMigration(version=42, advanced=True, body="""#!/bin/bash\necho Hello World > testspace/test_output\n""")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        migrator.applyMigrations([target])
        self.assertVersion(42)
        self.assertFileExists('test_output')
    
    def testPipesAdvancedOutput(self):
        creator = MigrationCreator('migration_test', testLocation())
        target = creator.createMigration(version=42, advanced=True, body="""#!/bin/bash\necho "create table xxx (yyy integer primary key);" """)
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        migrator.applyMigrations([target])
        self.assertVersion(42)
        self.assertColumnExists('xxx', 'yyy')
    
    def testEmptyUpFile(self):
        creator = MigrationCreator('migration_test', testLocation())
        target1 = creator.createMigration(version=17, body="""select * from __mig_version__""")
        target2 = creator.createMigration(version=23, body="""""")
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        self.assertRaisesRegexp(RuntimeError, "Invalid migration: Up file is empty", migrator.applyMigrations, ([target1, target2]))
        self.assertVersion(17)
    
    def testMissingUpFile(self):
        creator = MigrationCreator('migration_test', testLocation())
        target1 = creator.createMigration(version=17, body="""select * from __mig_version__""")
        target2 = creator.createMigration(version=23, body="""""")
        os.remove(testLocation('migration_test',target2,'up'))
        conf = Config()
        conf.fromMap(testConfig)
        migrator = MigrationApplier(testLocation(), conf)
        self.assertRaisesRegexp(RuntimeError, "Invalid migration: Up file not found", migrator.applyMigrations, ([target1, target2]))
        self.assertVersion(17)
