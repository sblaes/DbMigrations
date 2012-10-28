#!/usr/bin/env python

from distutils.core import setup
from dbmigrations.settings import VERSION

setup(name='DbMigrations',
    version=VERSION,
    description='Database Migrations Python Module',
    url='https://github.com/zfjagann/DbMigrations',
    packages=['dbmigrations'])