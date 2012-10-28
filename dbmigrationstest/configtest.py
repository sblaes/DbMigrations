from dbmigrations import Config
from dbmigrationstest import TestCase

class ConfigTest(TestCase):
    def testPutAndGet(self):
        conf = Config()
        conf.put('hello', 'world')
        self.assertTrue(conf.has('hello'))
        self.assertEquals('world', conf.get('hello'))

    def testOperators(self):
        conf = Config()
        conf['hello'] = 'world'
        self.assertTrue('hello' in conf)
        self.assertEquals('world', conf['hello'])

    def testIterator(self):
        conf = Config()
        conf['hello'] = 'world'
        for k, v in conf:
            self.assertEquals(k, 'hello')
            self.assertEquals(v, 'world')

    def testFromMapWithPrefix(self):
        conf = Config()
        env = {'prefix_hello':'world', 'nonprefix_foo':'bar'}
        conf.fromMap(env, 'prefix_')
        self.assertFalse(conf.has('prefix_hello'))
        self.assertFalse(conf.has('nonprefix_foo'))
        self.assertTrue(conf.has('hello'))
        self.assertFalse(conf.has('foo'))
        self.assertEquals('world', conf.get('hello'))

    def testFromMapLowercase(self):
        conf = Config()
        env = {'prefix_hElLo':'world'}
        conf.fromMap(env, 'prefix_')
        self.assertFalse(conf.has('hElLo'))
        self.assertTrue(conf.has('hello'))
        self.assertEquals('world', conf.get('hello'))

    def testFromMapWithoutPrefix(self):
        conf = Config()
        conf['hello'] = 'world'
        env = {'hello':'jello', 'foo':'bar'}
        conf.fromMap(env)
        self.assertTrue('hello' in conf)
        self.assertTrue('foo' in conf)
        self.assertEquals('jello', conf['hello'])
        self.assertEquals('bar', conf['foo'])
