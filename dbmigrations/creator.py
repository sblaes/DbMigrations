import currtime, datetime
import os
import stat
from logger import getLogger, error
from config import Config


HEADER_TEMPLATE = """\
Migration Created: {date}
"""


def initOptionParser(parser):
    '''Initialize the subparser for MigrationCreator.'''
    parser.add_argument('-a', '--advanced', action="store_true", dest="advanced", help='Create an advanced migration.')
    parser.add_argument('-b', '--basedir', dest='basedir', default=None, help='Specify the migrations base directory.')
    parser.add_argument('-d', '--db', '--database', dest='database', default=None, help='Specify the database name.')
    parser.add_argument('-v', dest='version', help='Specify the migration version.')
    parser.set_defaults(options=[],host=None,port=None,user=None)


def main(args):
    conf = Config()
    conf.initAll(args, basedir=args.basedir)

    if conf['database'] is None:
        error('Invalid database: %s' % conf['database'])
        return
    if conf['basedir'] is None:
        error('Invalid migration base directory: %s' % conf['basedir'])
        return
    creator = MigrationCreator(conf['database'], conf['basedir'])
    creator.createMigration(advanced=args.advanced, version=args.version, header=getDefaultHeader())


def getDefaultHeader():
    date_str = datetime.datetime.utcnow().isoformat()
    return HEADER_TEMPLATE.format(date=date_str)


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

    def createMigration(self, advanced=False, body=None, version=None, args=None, header=None):
        if self.database is None:
            raise RuntimeError("Database name must be provided.")
        if header is not None:
            file_contents = "\n".join(["-- " + s for s in header.splitlines()]) + "\n\n"
        else:
            file_contents = ""
        if body is not None:
            file_contents += (body + "\n")
        elif args is not None:
            file_contents += self.migrationBody(args) + "\n"
        if version is None:
            version = self.getVersion()
        else:
            version = str(version)
        self.createFolder(self.basedir)
        self.createFolder(os.path.join(self.basedir, self.database))
        self.createFolder(os.path.join(self.basedir, self.database, version))
        upTarget = os.path.join(self.basedir, self.database, version, 'up')
        self.logger.info("Created migration version %s at %s" % (version, upTarget))
        self.createFile(upTarget, file_contents, advanced)
        return version

    def getVersion(self):
        return str(currtime.getTime())

    def migrationBody(self, args):
        if args is None or len(args) == 0:
            return self.sampleUpFile()
        table_name = "SampleTable"
        if ':' not in args[0]:
            table_name = args[0]
        migration = "create table %s (" % table_name
        first = True
        for command in args[1:]:
            if not first:
                migration += ',\n'
            else:
                migration += '\n'
                first = False
            if ':' in command:
                words = command.split(':', 1)
                migration += "    %s %s" % (words[0], words[1])
            else:
                self.logger.warn('Unknown command: '+command)
        migration += "\n    );"
        return migration
