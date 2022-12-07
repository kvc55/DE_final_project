import sys
import unittest

import pandas as pd

sys.path.append('C:/Users/karen/Desktop/final_project/DE_final_project')

from src.dbmodules import Database

class DBmodules(unittest.TestCase):
    """Postgrest test modules."""

    def setUp(self):
        """Setup database connection.
        """

        #set test parameters of connection
        user="postgres"
        password="root"
        host="localhost"
        dbname="test"

        db = Database(user,password,host,dbname)
        self.test_db= db

    def test_bulkInsert(self):
        """Test insert table.
        """
        dataset = pd.DataFrame({
            'id': [1, 2, 3],
            'customer': ['Juan', 'Pedro', 'Maria']
        })
        assert self.test_db.bulkInsert(dataset, "id")        

    def test_fetchByTable(self):
        """Test fetch table.
        """
        assert self.test_db.fetchByTable("id")

    def test_fetchByQuery(self):
        """Test fetch table.
        """
        assert self.test_db.fetchByQuery("SELECT * FROM id")

    def test_dinorderquery(self):
        """Test fetch table.
        """
        assert self.test_db.dinorderquery("id", id='ASC')

    def test_dinfilterqueryand(self):
        """Test fetch table.
        """
        assert self.test_db.dinfilterqueryand("id", id='ASC')

    def test_dinfilterqueryor(self):
        """Test fetch table.
        """
        assert self.test_db.dinfilterqueryor("id", id='ASC')


if __name__ == '__main__':
    unittest.main()
