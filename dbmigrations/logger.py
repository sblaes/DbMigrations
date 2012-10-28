import datetime
import inspect
import os.path

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

DEFAULT_LOG_LEVEL = INFO

def getLogger():
    logger = Logger(DEFAULT_LOG_LEVEL)
    loggers.append(logger)
    return logger

def setDefaultLogLevel(level):
    DEFAULT_LOG_LEVEL = level

def disableLogging():
    for logger in loggers:
        logger.level = NONE

class Logger:
    def __init__(self,level):
        self.level = level

    def setLevel(self, level):
        self.level = level

    def merge(self, messages):
        return messages

    def logger(self, logLevel, message, trace=False):
        if(self.level.value <= logLevel.value):
            time = datetime.datetime(1,1,1).now()
            result = time.isoformat(' ') + ' ' + logLevel.name + ': ' + message
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
