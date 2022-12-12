import sys
import unittest

import pandas as pd

sys.path.append('C:/Users/karen/Desktop/final_project/DE_final_project')

from src.dbmodules import Database

class DBmodules(unittest.TestCase):
    """Postgrest test modules."""

    def setUp(self):
        """Setup database connection and dataset for test.
        """

        # Set test parameters of connection
        user="postgres"
        password="root"
        host="localhost"
        dbname="test"

        # Set test connection
        db = Database(user,password,host,dbname)
        self.test_db= db

        # Set test dataset
        self.dataset = pd.DataFrame({
            'customer_unique_id': [1, 2, 3],
            'customer_city': ['rio de janeiro', 'sao paulo', 'brasilia']
        })
 
    def test_bulkInsert(self):
        """Test insert table.
        """
        assert self.test_db.bulkInsert(self.dataset, "customer_unique_id")        

    def test_fetchByTable(self):
        """Test fetch table.
        """
        assert self.test_db.fetchByTable("customer_unique_id")

    def test_fetchByQuery(self):
        """Test fetch query.
        """
        assert self.test_db.fetchByQuery("SELECT * FROM customer_unique_id")

    def test_dinorderquery(self):
        """Test order query.
        """
        assert self.test_db.dinorderquery("customer_unique_id", id= 'DESC')

    def test_dinfilterqueryand(self):
        """Test filter AND query.
        """
        assert self.test_db.dinfilterqueryand("customer_unique_id", id= '>2')

    def test_dinfilterqueryor(self):
        """Test filter query.
        """
        assert self.test_db.dinfilterqueryor("customer_city", city= 'brasilia')


if __name__ == '__main__':
    unittest.main()
