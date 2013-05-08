from dbmigrations import Config, MigrationCreator, MigrationApplier
from testhelper import TestCase, locationInTestspace, testConfig

class PgPluginTest(TestCase):

    def testInvalidDatabase(self):
        conf = Config()
        conf.fromMap(testConfig)
        creator = MigrationCreator('asdf', locationInTestspace())
        target = creator.createMigration()
        migrator = MigrationApplier(locationInTestspace(), conf)
        self.assertRaises(BaseException, migrator.applyMigration, target)