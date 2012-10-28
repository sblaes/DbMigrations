from dbmigrations import PgPlugin
from dbmigrations.helper import makePath
from dbmigrations.config import Config
from dbmigrations.logger import getLogger
import os

def initOptionParser(parser):
    parser.add_argument('-o',nargs=2,action='append',dest='options',metavar=('KEY','VALUE'),help='Specify migrator options.')
    parser.add_argument('-b','--basedir',dest='basedir',help='Specify the migrations base directory.')
    parser.add_argument('-v','--version',dest='version',help='Force application of a specific version.')
    parser.add_argument('--env-prefix',dest='prefix',help='Specify the environment prefix.')

logger = getLogger()

def main(args):
    conf = Config()
    conf.initAll(args)
    if(args.basedir == None):
        args.basedir = '.'
    if(not(os.path.exists(args.basedir))):
        logger.error('Invalid migration base director: %s' % args.basedir)
        return
    migrator = MigrationApplier(args.basedir, conf)
    if(args.version == None):
        migrator.applyAllMigrations()
    else:
        migrator.applyMigration(args.version)

class MigrationApplier:
    def __init__(self, basedir, config):
        self.config = config
        self.basedir = basedir
        self.initializePlugin()

    def getUpFile(self, version):
        return makePath(self.basedir, self.config['database'], version, 'up')

    def applyAllMigrations(self):
        versions = os.listdir(self.basedir+'/'+self.config['database'])
        self.applyMigrations(versions)

    def applyMigrations(self, versions):
        sortedVersions = sorted(versions)
        self.plugin.openSession()
        try:
            for version in sortedVersions:
                if(version > self.plugin.getLatestVersion()):
                    self.applyMigration(version)
        finally:
            if(self.plugin.isOpen()):
                logger.warn('Migration '+version+' failed. Rolling back.')
                self.plugin.rollbackTransaction()
            self.plugin.closeSession()

    def applyMigration(self, version):
        self.plugin.openTransaction()
        logger.debug("Applying migration "+version)
        self.applyAtomicMigration(version)
        logger.debug("Migration "+version+" applied successfully.")
        self.plugin.updateVersion(version)
        self.plugin.commitTransaction()

    def applySingleMigration(self, version):
        self.plugin.openSession()
        try:
            self.applyMigration(version)
        finally:
            if(self.plugin.isOpen()):
                logger.warn('Migration '+version+' failed. Rolling back.')
                self.plugin.rollbackTransaction()
            self.plugin.closeSession()

    def applyAtomicMigration(self, version):
        path = self.getUpFile(version)
        f = open(path,'r')
        stuff = f.read()
        f.close()
        self.plugin.execute(stuff)

    def initializePlugin(self):
        self.plugin = None
        adapter = self.config['adapter']
        if(adapter == 'postgresql'):
            self.plugin = PgPlugin(self.config)
        else:
            raise RuntimeError("Invalid database adapter: "+adapter)
        return adapter
