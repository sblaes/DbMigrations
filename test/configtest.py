from dbmigrations import Config
from testhelper import TestCase, Bunch

class ConfigTest(TestCase):
    def testPutAndGet(self):
        conf = Config()
        conf.put('hello', 'world')
        self.assertTrue(conf.has('hello'))
        self.assertEqual('world', conf.get('hello'))

    def testOperators(self):
        conf = Config()
        conf['hello'] = 'world'
        self.assertTrue('hello' in conf)
        self.assertEqual('world', conf['hello'])

    def testIterator(self):
        conf = Config()
        conf['hello'] = 'world'
        for k, v in conf:
            self.assertEqual(k, 'hello')
            self.assertEqual(v, 'world')

    def testFromMapWithPrefix(self):
        conf = Config()
        env = {'prefix_hello':'world', 'nonprefix_foo':'bar'}
        conf.fromMap(env, 'prefix_')
        self.assertFalse(conf.has('prefix_hello'))
        self.assertFalse(conf.has('nonprefix_foo'))
        self.assertTrue(conf.has('hello'))
        self.assertFalse(conf.has('foo'))
        self.assertEqual('world', conf.get('hello'))

    def testFromMapLowercase(self):
        conf = Config()
        env = {'prefix_hElLo':'world'}
        conf.fromMap(env, 'prefix_')
        self.assertFalse(conf.has('hElLo'))
        self.assertTrue(conf.has('hello'))
        self.assertEqual('world', conf.get('hello'))

    def testFromMapWithoutPrefix(self):
        conf = Config()
        conf['hello'] = 'world'
        env = {'hello':'jello', 'foo':'bar'}
        conf.fromMap(env)
        self.assertTrue('hello' in conf)
        self.assertTrue('foo' in conf)
        self.assertEqual('jello', conf['hello'])
        self.assertEqual('bar', conf['foo'])

    def testPrecedence(self):
        bucket = {'database':'mydb', 'options':{}, 'basedir':'.', 'prefix':'MIG_', 'host':'localhost', 'port':5432, 'user':'dbmigrations'}
        env = {'database':'otherdb'}
        conf = Config()
        conf.initAll(Bunch(bucket), env)
        self.assertEqual('mydb', conf['database'])

    def testReadDotfile(self):
        class TestConfig(Config):
            def readFromDotfile(conf):
                conf.put('basedir', 'mybasedir')
                conf.put('database', 'mydb')
                conf.put('host', 'dbhost')
                conf.put('port', 42)
                conf.put('user', 'dbuser')
        bucket = {'database':None, 'options':{}, 'prefix':'MIG_', 'host':None, 'port':5432, 'user':'dbmigrations'}
        conf = TestConfig()
        conf.initAll(Bunch(bucket), {})
        self.assertEqual('mydb', conf['database'])
        self.assertEqual('mybasedir', conf['basedir'])
        self.assertEqual('dbhost', conf['host'])