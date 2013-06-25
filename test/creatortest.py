import os
from dbmigrations import MigrationCreator
from testhelper import locationInTestspace, TestCase

class CreateTest(TestCase):

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
        with open(locationInTestspace('zyxw', target, 'up'), 'r') as f:
            self.assertEquals("-- Sample Up migration file.\n", f.readline())

    def testCreatesMetaData(self):
        migrator = MigrationCreator('zyxw', locationInTestspace())
        target = migrator.createMigration()
        self.assertFileExists('zyxw', target, 'meta.json')
        wholeFile = ''
        with open(locationInTestspace('zyxw', target, 'meta.json'), 'r') as f:
            wholeFile = f.read()
        self.assertEquals('{\n    "note": "Sample meta file."\n}', wholeFile)

    def testCreatesTable(self):
        migrator = MigrationCreator('zyxw', locationInTestspace())
        target = migrator.createMigration(args=['tableName','column:type','column2:type2'])
        self.assertFileExists('zyxw', target, 'up')
        wholeFile = ''
        with open(locationInTestspace('zyxw', target, 'up'), 'r') as f:
            wholeFile = f.read()
        fileContent = """create table tableName (\n    column type,\n    column2 type2\n    );"""
        self.assertEqual(fileContent, wholeFile)
