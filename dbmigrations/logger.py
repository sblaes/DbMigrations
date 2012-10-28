"""Simply logging library for python.
Loggers can be created by calling getLogger.

The following levels are defined, in order:
    ALL
    DEBUG
    INFO
    WARN
    SEVERE
    ERROR
    FATAL
    NONE

Loggers will only print messages registered at a logging level equal to or greater than
the logger's current level.

Log levels SEVERE and FATAL will print stack traces of their callers.

For example:

>>> from dbmigrations.logger import getLogger

>>> logger = getLogger('consoleLogger','INFO')

>>> logger.info('This is an info message.')
INFO consoleLogger: This is an info message.

>>> logger.debug('This is a debug message.')

>>> logger.severe('This is a severe message.')
SEVERE consoleLogger: This is a severe message.
    <stdin>:1(<module>)

To make log management easy for entry-level functions, a master logger
is also provided, and can be used by calling the functions debug, info, warn, severe, error, and fatal.
"""

import datetime
import inspect
import os.path
from dbmigrations import settings

class LogLevel:
    def __init__(self,value,name):
        self.value = value
        self.name = name

ALL = LogLevel(0,'ALL')
DEBUG = LogLevel(1,'DEBUG')
INFO = LogLevel(2,'INFO')
WARN = LogLevel(3,'WARN')
SEVERE = LogLevel(4,'SEVERE')
ERROR = LogLevel(5,'ERROR')
FATAL = LogLevel(6,'FATAL')
NONE = LogLevel(7,'NONE')

loggers = []

def getLogger(name,levelName=settings.DEFAULT_LOG_LEVEL):
    '''Create a logger with the given name and log level.'''
    logger = Logger(fromName(levelName),name)
    loggers.append(logger)
    return logger

def fromName(name):
    '''Returns the logging level object with the given name.'''
    if(name=='ALL'):
        return ALL
    if(name=='DEBUG'):
        return DEBUG
    if(name=='INFO'):
        return INFO
    if(name=='WARN'):
        return WARN
    if(name=='SEVERE'):
        return SEVERE
    if(name=='ERROR'):
        return ERROR
    if(name=='FATAL'):
        return FATAL
    if(name=='NONE'):
        return NONE

def disableLogging():
    '''Disables all loggers created with getLogger, and sets the default log level to NONE.

    This can be used by tests to disable output.'''
    settings.DEFAULT_LOG_LEVEL = "NONE"
    for logger in loggers:
        logger.level = NONE

class Logger:
    '''Logger class for filtered logging output.
    '''
    def __init__(self,level,name):
        self.level = level
        self.name = name

    def setLevel(self, level):
        self.level = level

    def merge(self, messages):
        return messages

    def logger(self, logLevel, message, trace=False):
        if(self.level.value <= logLevel.value):
            result = logLevel.name + ' ' + self.name + ': ' + message
            print(result)
            if(trace):
                for frame in inspect.getouterframes(inspect.currentframe())[2:]:
                    frameText = ''
                    frameText += "{}:{}({})".format(frame[1],frame[2],frame[3])
                    print('    '+frameText)

    def debug(self, messages):
        self.logger(DEBUG, self.merge(messages))

    def info(self, messages):
        self.logger(INFO, self.merge(messages))

    def warn(self, messages):
        self.logger(WARN, self.merge(messages))

    def severe(self, messages):
        self.logger(SEVERE, self.merge(messages),trace=True)

    def error(self, messages):
        self.logger(ERROR, self.merge(messages))

    def fatal(self, messages):
        self.logger(FATAL, self.merge(messages),trace=True)

master_logger = getLogger('<module>')

def debug(self, messages):
    '''Print a debug message on the master logger.'''
    master_logger.debug(message)

def info(self, messages):
    '''Print an info message on the master logger.'''
    master_logger.info(message)

def warn(self, messages):
    '''Print a warning message on the master logger.'''
    master_logger.warn(message)

def severe(self, messages):
    '''Print a severe message on the master logger.'''
    master_logger.severe(message)

def error(self, messages):
    '''Print an error message on the master logger.'''
    master_logger.error(message)

def fatal(self, messages):
    '''Print a fatal message on the master logger.'''
    master_logger.fatal(message)