#!/usr/bin/env python

from setuptools import setup
from dbmigrations.settings import VERSION

setup(name='DbMigrations',
    version=VERSION,
    description='Database Migrations Python Module',
    url='https://github.com/zfjagann/DbMigrations',
    packages=['dbmigrations'],
    test_suite='dbmigrations.test')