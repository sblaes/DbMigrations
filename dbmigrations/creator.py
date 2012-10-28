import currtime
import os
import stat
from dbmigrations.logger import getLogger

def initOptionParser(parser):
    parser.add_argument('-a','--advanced',action="store_true",dest="advanced",help='Create an advanced migration.')
    parser.add_argument('-b','--basedir',dest='basedir',default='.',help='Specify the migrations base directory.')
    parser.add_argument('-d','--db','--database',dest='database',default=None,help='Specify the database name.',required=True)
    parser.add_argument('-v','--version',dest='version',help='Specify the migration version.')

def main(args):
    if(args.basedir == None):
        logger.error('Invalid migration base directory: %s' % args.basedir)
        return
    creator = MigrationCreator(args.database, args.basedir)
    creator.createMigration(advanced=args.advanced,version=args.version)

logger = getLogger()

class MigrationCreator:
    def __init__(self, database, basedir):
        self.database = database
        self.basedir = basedir

    def createFolder(self, filename):
        if(not(os.path.exists(filename))):
            os.mkdir(filename)

    def createFile(self, filename, body, advanced):
        if(not(os.path.exists(filename))):
            f = open(filename, 'w')
            if(body == None):
                f.write(self.sampleUpFile())
            else:
                f.write(body)
            f.close()
        if(advanced):
            # 755
            permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
            os.chmod(filename, permissions)

    def createMigration(self, advanced=False, body=None, version=None):
        if(self.database == None):
            raise RuntimeError("Database name must be provided.")
        name = ""
        if(version == None):
            name = self.getVersion()
        else:
            name = str(version)
        self.createFolder(self.basedir)
        self.createFolder(self.basedir + "/" + self.database)
        self.createFolder(self.basedir+"/"+self.database+"/"+name)
        target = self.basedir+"/"+self.database+"/"+name + "/up"
        #print "Created migration version %s at %s" % (name, target)
        self.createFile(target, body, advanced)
        return name

    def getVersion(self):
        return str(currtime.getTime())

    def sampleUpFile(self):
        return "-- Sample Up migration file.\n"

    def sampleDownFile(self):
        return "-- Sample Down migration file.\n"
