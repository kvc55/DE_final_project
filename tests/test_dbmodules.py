import sys
import os
import unittest

import pandas as pd

# Import ENV variables.
from dotenv import load_dotenv, find_dotenv
load_dotenv (find_dotenv('../config/.env'))

# Declare root path: pulled from ENV file.
sys.path.append(os.getenv("ROOT_PATH"))

from src.dbmodules import Database

class DBmodules(unittest.TestCase):
    """Postgrest test modules."""

    def setUp(self):
        """Setup database connection.
        """

        # Set test parameters of connection
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        dbname = os.getenv('DBNAME')

        # Set test connection
        db = Database(user, password, host, dbname)
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

