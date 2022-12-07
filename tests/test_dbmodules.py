import unittest
from dbmodules import Database
import pandas as pd

class DBmodules(unittest.TestCase):
    """Postgrest test modules."""

    def setUp(self):
        """Setup database connection.
        """
        #tset test data
        tablename="customer_id"
        #set test parameters of connection
        user="user"
        password="password"
        host="localhost"
        dbname="database"

        db = Database(user,password,host,dbname)
        test_db= db
        self.test_db
        

    def test_fetchByTable(self):
        """Test fetch table.
        """
        assert self.test_db.fetchByTable("nombre de tabla")

    def bulkInsert(self):
        """Test insert table.
        """
        dataset = pd.DataFrame()
        assert self.test_db.fetchByTable(dataset, "nombre de tabla")

    #def tearDown(self):
        #if self.connection is not None and self.connection.is_connected():
            #self.connection.close()

    #def test_connection(self):
        #self.assertTrue(self.connection.is_connected())

if __name__ == '__main__':
    unittest.main()
