#!/usr/bin/env python

class FakeDatabasePlugin:

    def __init__(self, testClass, currentVersion=None, failOn=None):
        self.testClass = testClass
        self.currentVersion = None
        if currentVersion != None:
            self.currentVersion = int(currentVersion)
        self.failOn = failOn
        self.transactionCommands = []
        self.committedCommands = []
        self.connectionOpen = False
        self.transactionOpen = False

    # Version Management
    def shouldApplyVersion(self, version):
        return self.currentVersion == None or self.currentVersion < int(version)

    def updateVersion(self, version):
        self.currentVersion = int(version)

    # Session Management
    def openSession(self):
        if self.connectionOpen:
            raise RuntimeError("Cannot open connection with open connection.")
        self.connectionOpen = True

    def closeSession(self):
        if not(self.connectionOpen):
            raise RuntimeError("Cannot close connection without open connection.")
        self.connectionOpen = False

    # Transaction Management
    def openTransaction(self):
        if not(self.connectionOpen):
            raise RuntimeError("Cannot open transaction without open connection.")
        if self.transactionOpen:
            raise RuntimeError("Cannot oepn transaction with open transaction.")
        self.transactionOpen = True

    def commitTransaction(self):
        if not(self.connectionOpen):
            raise RuntimeError("Cannot commit transaction without open connection.")
        if not(self.transactionOpen):
            raise RuntimeError("Cannot commit transaction without open transaction.")
        for f in self.transactionCommands:
            self.committedCommands.append(f)
        self.transactionOpen = False
        self.transactionCommands = []

    def rollbackTransaction(self):
        if not(self.connectionOpen):
            raise RuntimeError("Cannot rollback transaction without open connection.")
        if not(self.transactionOpen):
            raise RuntimeError("Cannot rollback transaction without open transaction.")
        self.transactionCommands = []
        self.transactionOpen = False

    def isOpen(self):
        return self.connectionOpen and self.transactionOpen

    # Command Execution
    def execute(self, stuff):
        if not(self.connectionOpen):
            raise RuntimeError("Cannot execute command without open connection.")
        if not(self.transactionOpen):
            raise RuntimeError("Cannot execute command without open transaction.")
        if stuff == self.failOn:
            raise RuntimeError("Failing on command for test")
        self.transactionCommands.append(stuff)

    def commandWasExecuted(self, stuff):
        return stuff in self.committedCommands

    def assertCommandWasExecuted(self, command):
        self.testClass.assertTrue(self.commandWasExecuted(command), "Command '" + command + "' was not executed")

    def assertNoCommandWasExecuted(self):
        self.testClass.assertEqual(0, len(self.committedCommands), 'Commands were executed when they shouldn\'t have.')

    def assertCommandWasNotExecuted(self, command):
        self.testClass.assertFalse(self.commandWasExecuted(command), "Command '" + command + "' was executed")

    def assertCurrentVersion(self, version):
        self.testClass.assertEqual(version, self.currentVersion, 'Expected version: '+str(version)+' but actual: '+str(self.currentVersion))

class FakeMultiPlugin(FakeDatabasePlugin):



    def __init__(self, testClass, currentVersion=None, failOn=None):
        FakeDatabasePlugin.__init__(self, testClass, None, failOn)
        self.versions = []
        if currentVersion != None:
            self.versions.append(currentVersion)

    # Version Management
    def shouldApplyVersion(self, version):
        return version not in self.versions

    def updateVersion(self, version):
        self.versions.append(version)

    def assertCurrentVersion(self, version):
        self.testClass.assertIn(str(version), self.versions)