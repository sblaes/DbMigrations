#!/usr/bin/env python

class DbPlugin:

    # Version Management
    def shouldApplyVersion(self, version):
        raise NotImplementedError("Cannot evaluate unimplemented function shouldApplyVersion.")

    def updateVersion(self, version):
        raise NotImplementedError("Cannot evaluate unimplemented function updateVersion.")

    # Session Management
    def openSession(self):
        raise NotImplementedError("Cannot evaluate unimplemented function openSession.")

    def closeSession(self):
        raise NotImplementedError("Cannot evaluate unimplemented function closeSession.")

    # Transaction Management
    def openTransaction(self):
        raise NotImplementedError("Cannot evaluate unimplemented function openTransaction.")

    def commitTransaction(self):
        raise NotImplementedError("Cannot evaluate unimplemented function commitTransaction.")

    def rollbackTransaction(self):
        raise NotImplementedError("Cannot evaluate unimplemented function rollbackTransaction.")

    def isOpen(self):
        raise NotImplementedError("Cannot evaluate unimplemented function isOpen.")

    # Command Execution
    def execute(self, stuff):
        raise NotImplementedError("Cannot evaluate unimplemented function execute.")
