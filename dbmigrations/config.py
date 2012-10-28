class Config:
    '''Configuration class that behaves like a dict object, but with an additional helper function to allow for reading arguments from a dictionary with a prefix.'''
    def __init__(self, options=None):
        if(options == None):
            options = {}
        self.options = options

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

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return self.has(key)


    def __iter__(self):
        return self.options.iteritems()