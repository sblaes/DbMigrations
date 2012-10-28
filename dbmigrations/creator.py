import currtime
import os
import stat

def initOptionParser(parser):
    parser.add_argument('-a','--advanced',action="store_true",dest="advanced",help='Create an advanced migration.')
    parser.add_argument('-b','--basedir',dest='basedir',default='.',help='Specify the migrations base directory.')
    parser.add_argument('-v','--version',dest='version',help='Specify the migration version.')

def main(args):
    creator = MigrationCreator(args.database, args.basedir)
    creator.createMigration(advanced=args.advanced,version=args.version)

class MigrationCreator:
    def __init__(self, database, basedir):
        self.database = database
        self.basedir = basedir

    def createFolder(self, filename):
        if(not(os.path.exists(filename))):
            os.mkdir(filename)

    def createFile(self, filename, advanced=False):
        if(not(os.path.exists(filename))):
            f = open(filename, 'w')
            f.write(self.sampleUpFile())
            f.close()
        if(advanced):
            # 755
            permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
            os.chmod(filename, permissions)

    def createMigration(self, advanced=False, version=None):
        if(self.database == None):
            raise RuntimeError("Database name must be provided.")
        name = ""
        if(version == None):
            name = self.getVersion()
        else:
            name = str(version)
        self.createFolder(self.basedir + "/" + self.database)
        self.createFolder(self.basedir+"/"+self.database+"/"+name)
        target = self.basedir+"/"+self.database+"/"+name + "/"
        self.createFile(target + "up", advanced)
        return target

    def getVersion(self):
        return str(currtime.getTime())

    def sampleUpFile(self):
        return "-- Sample Up migration file.\n"

    def sampleDownFile(self):
        return "-- Sample Down migration file.\n"
