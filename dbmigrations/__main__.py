#!/usr/bin/env python

import argparse
from dbmigrations import creator, applier
from sys import argv

parser = None
applyparser = None
createparser = None

def main():
    parser = makeOptionParser()
    args = parser.parse_args(argv[1:])
    args.func(args)

def makeOptionParser():
    parser = argparse.ArgumentParser(prog='dbmigrations')
    subparsers = parser.add_subparsers(title='subcommands')
    createparser = subparsers.add_parser('create',add_help=False)
    creator.initOptionParser(createparser)
    createparser.add_argument("--help",dest="help",action="store_true",help="show this help message and exit")
    createparser.set_defaults(func=creator.main,parser=createparser)
    applyparser = subparsers.add_parser('apply',add_help=False)
    applier.initOptionParser(applyparser)
    applyparser.add_argument("--help",dest="help",action="store_true",help="show this help message and exit")
    applyparser.set_defaults(func=applier.main,parser=applyparser)
    return parser

if(__name__=="__main__"):
    main()