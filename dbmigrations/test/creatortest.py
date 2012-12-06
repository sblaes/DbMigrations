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
        self.assertTrue(os.path.exists(testLocation('zyxw',target)))
        self.assertTrue(os.path.exists(testLocation('zyxw',target,'up')))

    def testCreateSpecificMigration(self):
        migrator = MigrationCreator("zyxw", testLocation())
        name = migrator.createMigration(version='abcdef')
        self.assertEquals('abcdef',name)
        target = testLocation('zyxw','abcdef','up')
        self.assertEquals('testspace/zyxw/abcdef/up', target)

    def testAdvancedMigration(self):
        migrator = MigrationCreator("zyxw", testLocation())
        name = migrator.createMigration(advanced=True)
        target = testLocation('zyxw',name,'up')
        self.assertExecutable(target)

    def testCreateMigrationWithBody(self):
        migrator = MigrationCreator("zyxw", testLocation())
        target = migrator.createMigration()
        f = open(testLocation('zyxw',target,'up'), 'r')
        line = f.readline()
        f.close()
        self.assertEquals("-- Sample Up migration file.\n", line)
