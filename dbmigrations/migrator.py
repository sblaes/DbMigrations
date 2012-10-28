#!/usr/bin/env python

from pgplugin import PgPlugin
import currtime
import os
import sys
from optparse import OptionParser, OptionGroup
import json
import time

class DbMigrator:
    def __init__(self, config):
        self.basedir = "."
        self.config = config
        self.plugin = None

    def setBaseDir(self, newBaseDir):
        self.basedir = newBaseDir