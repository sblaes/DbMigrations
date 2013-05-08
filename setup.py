#!/usr/bin/env python

from setuptools import setup
from dbmigrations.settings import VERSION

setup(name='DbMigrations',
    version=VERSION,
    description='Database Migrations Python Module',
    url='https://github.com/zfjagann/DbMigrations',
    packages=['dbmigrations'],
    install_requires=['setuptools','psycopg2'],
    tests_require=['nose'],
    test_suite='src')
