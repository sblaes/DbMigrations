import json
import os
import shutil
import unittest
import psycopg2
from dbmigrations.logger import disableLogging

testSpace = "testspace"
testDb = "migtest"
testPass = 'abcdef'
sampleConfigBody = {'hostname':'blergh','port':42,'database':'zyxw','password':'abcdef','user':'xxx','adapter':'yyy'}
sampleConfigFile = testSpace+"/config"
actualConfigBody = {'hostname':'localhost','port':5432,'database':testDb,'password':testPass,'user':'dbmigrations','adapter':'postgresql'}

def testLocation(*filenames):
    if(len(filenames) == 0):
        return testSpace
    else:
        return testSpace+"/"+("/".join(filenames))

def createSampleConfig():
    writeToFile(sampleConfigFile, json.dumps(sampleConfigBody))
    return sampleConfigFile

def createActualConfig():
    writeToFile(sampleConfigFile, json.dumps(actualConfigBody))
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

class TestCase(unittest.TestCase):
    def setUp(self):
        create(testLocation())
        disableLogging()

    def tearDown(self):
        delete(testLocation())
        self.dropTable('xxx')
        self.dropTable('aaa')
        self.dropTable('__mig_version__')

    def tableExists(self,table,database='migtest',user='dbmigrations',password='dbmigrations'):
        conn = psycopg2.connect(database=database,user=user,password=password)
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.tables where table_name = %s', (table,))
        result = cur.fetchone()
        conn.commit()
        conn.close()
        return result

    def assertTableExists(self,table,database='migtest',user='dbmigrations',password='dbmigrations'):
        self.assertNotEquals(None, self.tableExists(table,database,user,password))

    def assertColumnExists(self,table,column,database='migtest',user='dbmigrations',password='dbmigrations'):
        conn = psycopg2.connect(database=database,user=user,password=password)
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.columns where table_name = %s and column_name = %s', (table,column,))
        result = cur.fetchone()
        conn.commit()
        conn.close()
        self.assertNotEquals(None, result)

    def dropTable(self,table,database='migtest',user='dbmigrations',password='dbmigrations'):
        if(self.tableExists(table,database,user,password)):
            conn = psycopg2.connect(database=database,user=user,password=password)
            cur = conn.cursor()
            cur.execute('drop table '+table)
            conn.commit()
            conn.close()

    def assertTableNotExists(self,table,database='migtest',user='dbmigrations',password='dbmigrations'):
        conn = psycopg2.connect(database=database,user=user,password=password)
        cur = conn.cursor()
        cur.execute('select table_name from information_schema.tables where table_name = %s', (table,))
        result = cur.fetchone()
        conn.commit()
        conn.close()
        self.assertEquals(None, result)

    def assertVersion(self,version,database='migtest',user='dbmigrations',password='dbmigrations'):
        conn = psycopg2.connect(database=database,user=user,password=password)
        cur = conn.cursor()
        cur.execute('select version from __mig_version__')
        result = cur.fetchone()
        conn.commit()
        conn.close()
        self.assertNotEquals(None, result)
        self.assertEquals(str(version), result[0])

    def assertExecutable(self,filename):
        self.assertTrue(os.path.isfile(filename) and os.access(filename, os.X_OK))

    def assertFileExists(self, filename):
        self.assertTrue(os.path.isfile(filename))