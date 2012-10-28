#!/usr/bin/env python

class DbPlugin:
    def setOption(self, key, value):
        raise NotImplementedError("Cannot evaluate unimplemented function.")

    def openSession(self):
        raise NotImplementedError("Cannot evaluate unimplemented function.")

    def closeSession(self):
        raise NotImplementedError("Cannot evaluate unimplemented function.")

    def execute(self, stuff):
        raise NotImplementedError("Cannot evaluate unimplemented function.")

    def isOpen(self):
        raise NotImplementedError("Cannot evaluate unimplemented function.")