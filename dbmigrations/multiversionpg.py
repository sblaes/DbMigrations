#!/usr/bin/env python

from pgplugin import PgPlugin, VERSION_TABLE


class MultiVersionPg(PgPlugin):
    def __init__(self, config):
        PgPlugin.__init__(self, config)

    def shouldApplyVersion(self, version):
        return not self._alreadyApplied(str(version))

    def _alreadyApplied(self, version):
        wasOpen = self.isOpen()
        if(not(self.isOpen())):
            self.openTransaction()
        try:
            self.createVersionTable()
            self.cur.execute('select count(*) from '+VERSION_TABLE+' where version=\''+version+'\';')
            result = self.cur.fetchone()
            count = result[0]
            return count == 1
        finally:
            if(not(wasOpen)):
                self.commitTransaction()

    def updateVersion(self, version):
        wasOpen = self.isOpen()
        if(not(self.isOpen())):
            self.openTransaction()
        try:
            self.createVersionTable()
            self.cur.execute("insert into " + VERSION_TABLE + " (version) values (%s)", (version,))
        finally:
            if(not(wasOpen)):
                self.commitTransaction()
