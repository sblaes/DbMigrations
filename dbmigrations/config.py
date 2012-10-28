from dbmigrations import settings
import os
import json
import formatter

def initOptionParser(parser):
    parser.add_argument('-o',nargs=2,action='append',dest='options',metavar=('KEY','VALUE'),help='Specify migrator options.')
    parser.add_argument('-b','--basedir',dest='basedir',help='Specify the migrations base directory.')
    parser.add_argument('--env-prefix',dest='prefix',help='Specify the environment prefix.')

def main(args):
    conf = Config()
    conf.initAll(args)
    conf.printFull()

def readFromFile(conf, filename):
    if(os.path.exists(filename)):
        f = open(filename,'r')
        body = f.read()
        f.close()
        conf.fromMap(json.loads(body))    

class Config:
    '''Configuration class that behaves like a dict object, but with an additional helper function to allow for reading arguments from a dictionary with a prefix.'''
    def __init__(self, options=None):
        if(options == None):
            options = {}
        self.options = options

    def initAll(args):
        # Configuration File
        if(args.basedir != None):
            readFromFile(self, args.basedir + '/dbmigrations.conf')
        # Environment
        prefix = settings.ENVIRONMENT_PREFIX
        if(args.prefix != None):
            prefix = args.prefix
        self.fromMap(os.environ, prefix)
        # Arguments
        if(args.options != None):
            for pair in args.options:
                key = pair[0]
                value = pair[1]
                self[key] = value

    def put(self, key, value):
        '''Associate value to key in this config.'''
        self.options[key] = value

    def has(self, key):
        '''Returns true if the key exists in this config.'''
        return key in self.options

    def get(self, key):
        '''Get the value of the key in this config.'''
        return self.options[key]

    def fromMap(self, items, prefix=None):
        '''Read the current config from the given map. If prefix is provided, will ignore all options that do not begin with prefix, removing the prefix from the key before inserting the associated value.'''
        for k, v in items.iteritems():
            if(prefix != None and k.find(prefix,0,len(prefix)) == 0):
                key = k.replace(prefix, '', 1).lower()
                value = v
                self.put(key,value)
            elif prefix == None:
                self.put(k, v)

    def printFull(self):
        if(len(self.options) == 0):
            print("No options provided.")
        else:
            maxlength = 4
            for k, v in self:
                if(len(k) > maxlength):
                    maxlength = len(k)
            format = '{0:<'+str(maxlength+1)+'} {1}'
            print format.format('Key', 'Value')
            for k, v in self:
                print format.format(k, v)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return self.has(key)


    def __iter__(self):
        return self.options.iteritems()