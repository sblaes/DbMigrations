from dbmigrations import PgPlugin

def initOptionParser(parser):
    parser.add_argument('-o',nargs=2,action='append',dest='options',metavar=('KEY','VALUE'),help='Specify migrator options.')
    parser.add_argument('-b','--basedir',dest='basedir',help='Specify the migrations base directory.')
    parser.add_argument('-v','--version',dest='version',help='Force application of a specific version.')
    parser.add_argument('--env-prefix',dest='prefix',help='Specify the environment prefix.')

def main(args):
    print args
    print("Apply...")

class MigrationApplier:
    def __init__(self, adapter, host, port, database, user, password, basedir):
        self.adapter = adapter
        self.database = database
        self.hostname = host
        self.port = port
        self.user = user
        self.password = password
        self.basedir = basedir

    def applyMigration(self, migVersion):
        self.initializePlugin()
        self.plugin.openSession()
        try:
            self.applySingleMigration(migVersion)
            self.plugin.commit()
        finally:
            if(self.plugin.isOpen()):
                print("Migraiton failed. Rolling back.")
                self.plugin.rollback()
            self.plugin.closeSession()

    def applySingleMigration(self, migVersion):
        f = open(migVersion+'/up','r')
        stuff = f.read()
        f.close()
        print("Applying migration "+migVersion)
        self.plugin.execute(stuff)
        self.plugin.commit()
        print("Migration "+migVersion+" applied successfully.")

    def initializePlugin(self):
        self.plugin = None
        adapter = self.adapter
        if(adapter == 'postgresql'):
            self.plugin = PgPlugin()
            self.plugin.setOption('hostname', self.hostname)
            self.plugin.setOption('port', self.port)
            self.plugin.setOption('database', self.database)
            self.plugin.setOption('user', self.user)
            self.plugin.setOption('password', self.password)
        else:
            raise RuntimeError("Invalid database adapter: "+adapter)
        return adapter
