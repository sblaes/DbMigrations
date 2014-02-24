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

    def testCreateMigrationWithHeader(self):
        migrator = MigrationCreator("zyxw", locationInTestspace())
        header = "This is the header of the file."
        target = migrator.createMigration(header=header)
        with open(locationInTestspace('zyxw', target, 'up'), 'r') as f:
            self.assertEquals("-- " + header + "\n", f.readline())

    def testCreateMigrationWithBody(self):
        migrator = MigrationCreator("zyxw", locationInTestspace())
        body = "This is the body of the file."
        target = migrator.createMigration(body=body)
        with open(locationInTestspace('zyxw', target, 'up'), 'r') as f:
            self.assertEquals(body + "\n", f.readline())

    def testCreatesTable(self):
        migrator = MigrationCreator('zyxw', locationInTestspace())
        target = migrator.createMigration(args=['tableName','column:type','column2:type2'])
        self.assertFileExists('zyxw', target, 'up')
        wholeFile = ''
        with open(locationInTestspace('zyxw', target, 'up'), 'r') as f:
            wholeFile = f.read()
        fileContent = """create table tableName (\n    column type,\n    column2 type2\n    );\n"""
        self.assertEqual(fileContent, wholeFile)
