import currtime
import os

def initOptionParser(parser):
    parser.add_argument('-d','-db','--database',dest="database",help='Set the database name.')
    parser.add_argument('-a','--advanced',action="store_true",dest="advanced",help='Create an advanced migration.')
    parser.add_argument('-b','--basedir',dest='basedir',help='Specify the migraitons base directory.')
    return parser

def main(args):
    if(args.help):
        args.parser.print_help()
        return
    creator = MigrationCreator(args.basedir, args.database)
    creator.createMigration()

class MigrationCreator:
    def __init__(self, database, basedir):
        if(basedir == None):
            basedir = '.'
        self.database = database
        self.basedir = basedir

    def createFolder(self, filename):
        if(not(os.path.exists(filename))):
            os.mkdir(filename)

    def createFile(self, filename):
        if(not(os.path.exists(filename))):
            f = open(filename, 'w')
            f.write(self.sampleUpFile())
            f.close()

    def createMigration(self, version = None):
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
        self.createFile(target + "up")
        return target

    def getVersion(self):
        return str(currtime.getTime())

    def sampleUpFile(self):
        return "-- Sample Up migration file.\n"

    def sampleDownFile(self):
        return "-- Sample Down migration file.\n"
