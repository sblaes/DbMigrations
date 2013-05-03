from dbmigrations.logger import disableLogging
import json
import os
import psycopg2
import shutil
import unittest

sampleTestWorkspace = "testspace"
testDb = "migration_test"
testPass = 'dbmigrations'
testUser = 'dbmigrations'
sampleConfigBody = {'host':'blergh', 'port':42, 'database':'zyxw', 'password':'abcdef', 'user':'xxx', 'adapter':'yyy'}
sampleConfigFile = sampleTestWorkspace + "/config"

def locationInTestspace(*filenames):
    if(len(filenames) == 0):
        return sampleTestWorkspace
    else:
        return sampleTestWorkspace + "/" + ("/".join(filenames))

testConfig = {'host':'localhost', 'port':5432, 'database':testDb, 'password':testPass, 'user':testUser, 'adapter':'postgresql',
              'basedir':locationInTestspace()}

def createSampleConfig():
    writeToFile(sampleConfigFile, json.dumps(sampleConfigBody))
    return sampleConfigFile

def createActualConfig():
    writeToFile(sampleConfigFile, json.dumps(testConfig))
    return sampleConfigFile

def delete(location):
    if(os.path.exists(location)):
        shutil.rmtree(location)

def create(location):
    if(not(os.path.exists(location))):
        os.mkdir(location)

def writeToFile(filename, body):
    f = open(filename, 'w')
    f.write(body)
    f.close()

class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

class TestCase(unittest.TestCase):
    def setUp(self):
        create(locationInTestspace())
        disableLogging()

    def tearDown(self):
        delete(locationInTestspace())

    def tableExists(self, table, database='migration_test', user='dbmigrations', password='dbmigrations'):
        conn = psycopg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.tables where table_name = %s', (table,))
        result = cur.fetchone()
        conn.commit()
        conn.close()
        return result

    def assertTableExists(self, table, database='migration_test', user='dbmigrations', password='dbmigrations'):
        self.assertNotEquals(None, self.tableExists(table, database, user, password), "Table " + table + " does not exist")

    def assertColumnExists(self, table, column, database='migration_test', user='dbmigrations', password='dbmigrations'):
        conn = psycopg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.columns where table_name = %s and column_name = %s', (table, column,))
        result = cur.fetchone()
        conn.commit()
        conn.close()
        self.assertNotEquals(None, result, "Column " + table + "." + column + " does not exist")

    def dropTable(self, table, database='migration_test', user='dbmigrations', password='dbmigrations'):
        if(self.tableExists(table, database, user, password)):
            conn = psycopg2.connect(database=database, user=user, password=password)
            cur = conn.cursor()
            cur.execute('drop table ' + table)
            conn.commit()
            conn.close()

    def assertTableNotExists(self, table, database='migration_test', user='dbmigrations', password='dbmigrations'):
        conn = psycopg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.tables where table_name = %s', (table,))
        result = cur.fetchone()
        conn.commit()
        conn.close()
        self.assertEquals(None, result, "Table " + table + " exists")

    def assertVersion(self, version, database='migration_test', user='dbmigrations', password='dbmigrations'):
        conn = psycopg2.connect(database=database, user=user, password=password)
        cur = conn.cursor()
        cur.execute('select version from __mig_version__')
        result = cur.fetchone()
        conn.commit()
        conn.close()
        self.assertNotEquals(None, result, "Version not found in " + database)
        self.assertEquals(str(version), result[0], "Incorrect version found, expected " + str(version) + " but was " + result[0])

    def assertExecutable(self, filename):
        self.assertTrue(os.path.isfile(filename) and os.access(filename, os.X_OK), "File " + filename + " is not executable")

    def assertFileExists(self, *filenames):
        filename = apply(locationInTestspace, filenames)
        self.assertTrue(os.path.isfile(filename), "File " + filename + " does not exist")
    
    def assertFolderExists(self, *filenames):
        filename = apply(locationInTestspace, filenames)
        self.assertTrue(os.path.isdir(filename), "Directory " + filename + " does not exist")
