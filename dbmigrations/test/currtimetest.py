from testhelper import *
from dbmigrations.currtime import getDatestampFromTimestamp

class CurrtimeTest(TestCase):
    
    def testUtcTimestampsWork(self):
        datestamp = getDatestampFromTimestamp(1351066312)
        actual = "20121024081152"
        self.assertEquals(actual, datestamp)
