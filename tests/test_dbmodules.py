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
