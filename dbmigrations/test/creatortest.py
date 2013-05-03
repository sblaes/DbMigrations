import os
from dbmigrations import *
from testhelper import *

class CreateTest(TestCase):

    def tearDown(self):
        delete(locationInTestspace())

    def testSpaceExists(self):
        self.assertTrue(os.path.exists(locationInTestspace()))

    def testCreateMigration(self):
        migrator = MigrationCreator("zyxw", locationInTestspace())
        target = migrator.createMigration()
        self.assertTrue(os.path.exists(locationInTestspace('zyxw', target)))
        self.assertTrue(os.path.exists(locationInTestspace('zyxw', target, 'up')))

    def testCreateSpecificMigration(self):
        migrator = MigrationCreator("zyxw", locationInTestspace())
        name = migrator.createMigration(version='abcdef')
        self.assertEquals('abcdef', name)
        target = locationInTestspace('zyxw', 'abcdef', 'up')
        self.assertEquals('testspace/zyxw/abcdef/up', target)

    def testAdvancedMigration(self):
        migrator = MigrationCreator("zyxw", locationInTestspace())
        name = migrator.createMigration(advanced=True)
        target = locationInTestspace('zyxw', name, 'up')
        self.assertExecutable(target)

    def testCreateMigrationWithBody(self):
        migrator = MigrationCreator("zyxw", locationInTestspace())
        target = migrator.createMigration()
        f = open(locationInTestspace('zyxw', target, 'up'), 'r')
        line = f.readline()
        f.close()
        self.assertEquals("-- Sample Up migration file.\n", line)
