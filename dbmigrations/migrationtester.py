import os
from logger import error
from applier import MigrationApplier
from config import Config


def initOptionParser(parser):
    '''Initialize the subparser for MigrationTester.'''
    parser.add_argument('-o', nargs=2, action='append', dest='options', metavar=('KEY', 'VALUE'), help='Specify migrator options.')
    parser.add_argument('-b', '--basedir', dest='basedir', help='Specify the migrations base directory.')
    parser.add_argument('-v', '--version', dest='version', help='Force application of a specific version.')
    parser.add_argument('--env-prefix', dest='prefix', help='Specify the environment prefix.')
    parser.add_argument('-h', dest='host', help='Equivalent to `-o host HOST`.')
    parser.add_argument('-d', dest='database', help='Equivalent to `-o database DATABASE`.')
    parser.add_argument('-p', dest='port', help='Equivalent to `-o port PORT`.')
    parser.add_argument('-U', dest='user', help='Equivalent to `-o user USER`.')
    parser.add_argument('--noop', '--dry-run', dest='dry_run', help='Print versions of migrations but do not run them.')


def main(args):
    '''Run the migration applier using the given parsed command line arguments.'''
    conf = Config()
    conf.initAll(args)
    if args.basedir is None:
        args.basedir = '.'
    if not(os.path.exists(args.basedir)):
        error('Invalid migration base directory: %s' % args.basedir)
        return
    migrator = MigrationTester(args.basedir, conf, dry_run=args.dry_run)
    if args.version is None:
        migrator.applyAllMigrations()
    else:
        migrator.applySingleMigration(args.version)


class MigrationTestFailure(RuntimeError):
    def __init__(self, message):
        RuntimeError.__init__(self, message)


class MigrationTester(MigrationApplier):
    def getMigrationFile(self, version, name):
        return os.path.join(self.basedir, self.config['database'], version, name)

    def preRun(self, version, upfile):
        fixture_file = self.getMigrationFile(version, 'fixture')
        if os.path.exists(fixture_file):
            stdout, stderr, exitcode = self._execFile(self.getMigrationFile(version, 'fixture'))
            if exitcode != 0:
                raise MigrationTestFailure('Migration %s fixture exited with code %s.' % (version, exitcode))

    def postRun(self, version, upfile):
        test_file = self.getMigrationFile(version, 'test')
        if os.path.exists(test_file):
            stdout, stderr, exitcode = self._execFile(test_file)
            if exitcode != 0:
                raise MigrationTestFailure('Migration %s test failed with code %s: %s' % (version, exitcode, stdout.strip()))
        else:
            self.logger.warn('Migration %s has no test.' % version)
