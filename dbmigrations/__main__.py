#!/usr/bin/env python

import argparse
import creator, applier, config, settings, versionupgrader, migrationtester
from sys import argv

parser = None
applyparser = None
createparser = None


def main():
    parser = makeOptionParser()
    args = parser.parse_args(argv[1:])
    if(args.help):
        args.parser.print_help()
        return
    else:
        if args.prefix is not None:
            settings.ENVIRONMENT_PREFIX = args.prefix
        args.func(args)


def versionMain(args):
    print('DbMigrations ' + settings.VERSION)
    return


def makeOptionParser():
    parser = argparse.ArgumentParser(prog='dbmigrations')
    parser.set_defaults(print_version=False)
    parser.add_argument('--env-prefix', dest='prefix', default=None, help='set the environment prefix')

    subparsers = parser.add_subparsers(title='subcommands')
    version = subparsers.add_parser('version', add_help=False)
    version.set_defaults(print_version=True, help=False)

    combineParsers(subparsers, 'create', creator.main, creator.initOptionParser)
    combineParsers(subparsers, 'apply', applier.main, applier.initOptionParser)
    combineParsers(subparsers, 'upgrade-versions', versionupgrader.main, versionupgrader.initOptionParser)
    combineParsers(subparsers, 'version', versionMain)
    combineParsers(subparsers, 'test', migrationtester.main, migrationtester.initOptionParser)

    if(settings.PRINT_CONFIG_ENABLED):
        combineParsers(subparsers, 'print-config', config.main, config.initOptionParser)
    return parser


def combineParsers(subparsers, name, main, initParser=None):
    sub = subparsers.add_parser(name, add_help=False)
    if initParser is not None:
        initParser(sub)
    sub.add_argument("--help", dest="help", action="store_true", help="show this help message and exit")
    sub.set_defaults(func=main, parser=sub)


if(__name__ == "__main__"):
    main()
