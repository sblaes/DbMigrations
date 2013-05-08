#!/usr/bin/env python

from config import Config
import os
from applier import MigrationApplier
from logger import error, info
from multiversionpg import MultiVersionPg

def initOptionParser(parser):
    '''Initialize the subparser for MigrationApplier.'''
    parser.add_argument('-o', nargs=2, action='append', dest='options', metavar=('KEY', 'VALUE'), help='Specify migrator options.')
    parser.add_argument('-b', '--basedir', dest='basedir', help='Specify the migrations base directory.')
    parser.add_argument('--env-prefix', dest='prefix', help='Specify the environment prefix.')
    parser.add_argument('-h', dest='host', help='Equivalent to `-o host HOST`.')
    parser.add_argument('-d', dest='database', help='Equivalent to `-o database DATABASE`.')
    parser.add_argument('-p', dest='port', help='Equivalent to `-o port PORT`.')
    parser.add_argument('-U', dest='user', help='Equivalent to `-o user USER`.')

def main(args):
    '''Run the migration applier using the given parsed command line arguments.'''
    conf = Config()
    conf.initAll(args)
    if(args.basedir == None):
        args.basedir = '.'
    if(not(os.path.exists(args.basedir))):
        error('Invalid migration base directory: %s' % args.basedir)
        return
    migrator = MigrationApplier(args.basedir, conf)
    migrator.applyAllMigrations()
    migrator.plugin = MultiVersionPg(conf)
    versions = migrator.getMigrationVersions()
    try:
        migrator.plugin.openSession()
        migrator.plugin.openTransaction()
        migrator.plugin.execute('truncate __mig_version__;')
        for version in versions:
            migrator.plugin.updateVersion(version)
        migrator.plugin.commitTransaction()
    finally:
        if migrator.plugin.isOpen():
            migrator.plugin.rollbackTransaction()
        migrator.plugin.closeSession()
    info('Upgraded migrations to multi-version.')