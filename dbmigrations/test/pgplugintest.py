from dbmigrations import pgplugin, Config, MigrationCreator, MigrationApplier
from testhelper import TestCase, locationInTestspace, testConfig

class PgPluginTest(TestCase):

    def testInvalidDatabase(self):
        conf = Config()
        conf.fromMap(testConfig)
        creator = MigrationCreator('asdf', locationInTestspace())
        target = creator.createMigration()
        migrator = MigrationApplier(locationInTestspace(), conf)
        failed = True
        try:
            migrator.applyMigration(target)
        except BaseException:
            return
        self.fail('Migration for bad table did not fail.')