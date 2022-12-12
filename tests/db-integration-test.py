import sys
import unittest

import pandas as pd

# sys.path.append('C :/Users/karen/Desktop/final_project/DE_final_project')
sys.path.append('/home/cratag/dev/DE_final_project')

from src.dbmodules import Database
import src.etl_to_db as etl

class DBTest(unittest.TestCase):
    def setUp(self) -> None:
        """ Load data setUp """
        TEST_INPUT_DIR = 'data_input/'
        test_file_customer =  'olist_customers_dataset.csv'
        test_file_geolocation =  'olist_geolocation_dataset.csv'
        test_file_items =  'olist_order_items_dataset.csv'
        test_file_payments =  'olist_order_payments_dataset.csv'
        test_file_reviews =  'olist_order_reviews_dataset.csv'
        test_file_orders=  'olist_orders_dataset.csv'
        test_file_products=  'olist_products_dataset.csv'
        test_file_sellers=  'olist_sellers_dataset.csv'
        
        self.test_csv_customer = TEST_INPUT_DIR + test_file_customer
        self.test_csv_geolocation = TEST_INPUT_DIR + test_file_geolocation
        self.test_csv_items = TEST_INPUT_DIR + test_file_items
        self.test_csv_payments = TEST_INPUT_DIR + test_file_payments
        self.test_csv_reviews = TEST_INPUT_DIR + test_file_reviews
        self.test_csv_orders = TEST_INPUT_DIR + test_file_orders
        self.test_csv_products = TEST_INPUT_DIR + test_file_products
        self.test_csv_sellers = TEST_INPUT_DIR + test_file_sellers
        
        #set test parameters of connection
        user="postgres"
        password="postgres"
        host="localhost:5433"
        dbname="test"

        db = Database(user,password,host,dbname)
        self.test_db= db

    def test_etl_customers(self) -> None:
        result = etl.etl_customers(self.test_csv_customer)

        # Checks total columns 
        self.assertEqual((len(result.columns)), 4)

        # Checks not existence of dropped column
        self.assertNotIn(list(result.columns), ['customer_unique_id'])
        
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # Checks Exception handle
        with self.assertRaises(Exception):
            etl.etl_customers()


if __name__ == '__main__':
    unittest.main()
