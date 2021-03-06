'''Migration Applier class.

The migration applier class is responsible for applying migrations.
'''

from pgplugin import PgPlugin
from multiversionpg import MultiVersionPg
from config import Config
from logger import getLogger, error
import os
import subprocess
import sys


def initOptionParser(parser):
    '''Initialize the subparser for MigrationApplier.'''
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
    if(not(os.path.exists(args.basedir))):
        error('Invalid migration base directory: %s' % args.basedir)
        return
    migrator = MigrationApplier(args.basedir, conf, dry_run=args.dry_run)
    try:
        if args.version is None:
            migrator.applyAllMigrations()
        else:
            migrator.applySingleMigration(args.version)
    except MigrationError as e:
        print str(e)
        sys.exit(1)


class MigrationError(RuntimeError):
    def __init__(self, message, cause):
        self.message = message
        self.cause = cause

    def __str__(self):
        return self.message + "\nCaused by: " + str(self.cause)


class MigrationApplier:
    '''MigrationApplier class

    To apply groups of migrations, use applyAllMigrations() or applyMigrations(versions)

    To apply a specific migration version, use applySingleMigration(version)
    '''

    def __init__(self, basedir, config, dry_run=False):
        '''Create a MigrationApplier from the given base directory and configuration.

        The base directory must exist, and the configuration must contain ample
        information for the adapter to connect to the database.
        '''
        self.dry_run = dry_run
        self.config = config
        self.basedir = basedir
        self.initializePlugin()
        self.logger = getLogger('MigrationApplier')

    def getUpFile(self, version):
        '''Get the up file for a particular version.

        The up file is calculated as os.path.join(basedir,databasename,version,'up')
        '''
        return os.path.join(self.basedir, self.config['database'], version, 'up')

    def applyAllMigrations(self):
        '''Apply all migrations in the base directory in lexicographic order,
        starting with the first version after the current database version.
        '''
        self.applyMigrations(self.getMigrationVersions())

    def getMigrationVersions(self):
        return os.listdir(os.path.join(self.basedir, self.config['database']))

    def applyMigrations(self, versions):
        '''Apply a specific group of migrations in lexicographic order,
        starting with the first version after the current database version.
        '''
        sortedVersions = sorted(versions)
        self.plugin.openSession()
        try:
            for version in sortedVersions:
                if self.plugin.shouldApplyVersion(version):
                    self.applyMigration(version)
        finally:
            if(self.plugin.isOpen()):
                self.logger.error('Migration \'' + version + '\' failed. Rolling back.')
                self.plugin.rollbackTransaction()
            self.plugin.closeSession()

    def applyMigration(self, version, update_version=True):
        '''Apply a specific migration version.

        A database connection must already be established.
        '''
        if not self.dry_run:
            self.plugin.openTransaction()
        self.logger.info("Applying migration " + version)
        if not self.dry_run:
            path = self.getUpFile(version)
            try:
                self.preRun(version, path)
                if self.isAdvanced(path):
                    self.applyAdvancedMigration(path)
                else:
                    self.applySimpleMigration(path)
                self.postRun(version, path)
            except BaseException as e:
                raise MigrationError("The migration %s failed to apply." % version, e)
        self.logger.debug("Migration " + version + " applied successfully.")
        if not self.dry_run:
            if update_version:
                try:
                    self.plugin.updateVersion(version)
                except BaseException as e:
                    raise MigrationError("Could not update version number. Has this migration already been applied?", e)
            self.plugin.commitTransaction()

    def preRun(self, version, upfile):
        pass

    def postRun(self, version, upfile):
        pass

    def _execFile(self, path):
        proc = subprocess.Popen(path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = proc.communicate()
        stdout = result[0]
        stderr = result[1]
        retcode = proc.returncode
        return (stdout, stderr, retcode)

    def applyAdvancedMigration(self, path):
        stdout, stderr, exitcode = self._execFile(path)
        if(stderr and stderr != ''):
            self.logger.info('Advanced Migration stderr:')
            self.logger.infos(stderr)
            raise RuntimeError('Advanced migration failed.')
        if(stdout and stdout != ''):
            self.logger.debug("Piping to sql: '" + stdout + "'")
            self.plugin.execute(stdout)

    def applySimpleMigration(self, path):
        stuff = self.getMigrationBody(path).strip()
        if stuff == "":
            raise RuntimeError("Invalid migration: Up file is empty")
        self.plugin.execute(stuff)

    def getMigrationBody(self, path):
        if not(os.path.isfile(path)):
            raise RuntimeError("Invalid migration: Up file not found.")
        with open(path, 'r') as f:
            return f.read()

    def applySingleMigration(self, version):
        '''Apply a specific migration version, establishing and closing the database
        connection around the migration.

        This function is not to be used when applying large groups of migrations.
        Use applyMigrations or applyAllMigrations instead.
        '''
        self.plugin.openSession()
        try:
            self.applyMigration(version, update_version=False)
        finally:
            if(self.plugin.isOpen()):
                self.logger.error('Migration ' + version + ' failed. Rolling back.')
                self.plugin.rollbackTransaction()
            self.plugin.closeSession()

    def initializePlugin(self):
        '''Creates the database adapter from the current configuration.

        Raises a RuntimeError if the adapter is not recognized.
        '''
        self.plugin = None
        adapter = self.config['adapter']
        if adapter == 'postgresql':
            self.plugin = PgPlugin(self.config)
        elif adapter == 'multiversionpg':
            self.plugin = MultiVersionPg(self.config)
        else:
            raise RuntimeError("Invalid database adapter: " + adapter)
        return adapter

    def isAdvanced(self, filename):
        return os.path.isfile(filename) and os.access(filename, os.X_OK)
