import currtime
import os
import stat
from logger import getLogger, error

def initOptionParser(parser):
    '''Initialize the subparser for MigrationCreator.'''
    parser.add_argument('-a', '--advanced', action="store_true", dest="advanced", help='Create an advanced migration.')
    parser.add_argument('-b', '--basedir', dest='basedir', default='.', help='Specify the migrations base directory.')
    parser.add_argument('-d', '--db', '--database', dest='database', default=None, help='Specify the database name.')
    parser.add_argument('-v', dest='version', help='Specify the migration version.')

def main(args):
    if(args.database == None):
        error('Invalid database: %s' % args.database)
        return
    if(args.basedir == None):
        error('Invalid migration base directory: %s' % args.basedir)
        return
    creator = MigrationCreator(args.database, args.basedir)
    creator.createMigration(advanced=args.advanced, version=args.version)

class MigrationCreator:
    def __init__(self, database, basedir):
        self.database = database
        self.basedir = basedir
        self.logger = getLogger('MigrationCreator')

    def createFolder(self, filename):
        if(not(os.path.exists(filename))):
            os.mkdir(filename)

    def createFile(self, filename, body, advanced):
        if(not(os.path.exists(filename))):
            f = open(filename, 'w')
            f.write(body)
            f.close()
        if(advanced):
            # 755
            permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
            os.chmod(filename, permissions)

    def createMigration(self, advanced=False, body=None, version=None):
        if self.database == None:
            raise RuntimeError("Database name must be provided.")
        if body == None:
            body = self.sampleUpFile()
        if(version == None):
            version = self.getVersion()
        else:
            version = str(version)
        self.createFolder(self.basedir)
        self.createFolder(os.path.join(self.basedir, self.database))
        self.createFolder(os.path.join(self.basedir, self.database, version))
        upTarget = os.path.join(self.basedir, self.database, version, 'up')
        metaTarget = os.path.join(self.basedir, self.database, version, 'meta.json')
        self.logger.info("Created migration version %s at %s" % (version, upTarget))
        self.createFile(upTarget, body, advanced)
        self.createFile(metaTarget, self.sampleMetaFile(), advanced)
        return version

    def getVersion(self):
        return str(currtime.getTime())

    def sampleUpFile(self):
        return "-- Sample Up migration file.\n"

    def sampleDownFile(self):
        return "-- Sample Down migration file.\n"

    def sampleMetaFile(self):
        return '{\n    "note": "Sample meta file."\n}'
