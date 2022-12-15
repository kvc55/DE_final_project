import sys
import unittest
import datetime
import os 

import pandas as pd

# Import ENV variables.
from dotenv import load_dotenv, find_dotenv
load_dotenv (find_dotenv('../config/.env'))

# Declare root path: pulled from ENV file.
sys.path.append(os.getenv("ROOT_PATH"))

# Modules to test
from src.dbmodules import Database
import src.etl_to_db as etl

class DBTest(unittest.TestCase):
    @classmethod # Decorator to call setUpClass and set variables.
    def setUpClass(cls) -> None:
        """ Load data setUp once for this class"""

        # CSV datasets to populate DB.
        TEST_INPUT_DIR = f'{os.getenv("ROOT_PATH")}/tests/data_input/'
        test_file_customer =  'olist_customers_dataset.csv'
        test_file_geolocation =  'olist_geolocation_dataset.csv'
        test_file_items =  'olist_order_items_dataset.csv'
        test_file_payments =  'olist_order_payments_dataset.csv'
        test_file_reviews =  'olist_order_reviews_dataset.csv'
        test_file_orders=  'olist_orders_dataset.csv'
        test_file_products=  'olist_products_dataset.csv'
        test_file_sellers=  'olist_sellers_dataset.csv'
        
        cls.test_csv_customer = TEST_INPUT_DIR + test_file_customer
        cls.test_csv_geolocation = TEST_INPUT_DIR + test_file_geolocation
        cls.test_csv_items = TEST_INPUT_DIR + test_file_items
        cls.test_csv_payments = TEST_INPUT_DIR + test_file_payments
        cls.test_csv_reviews = TEST_INPUT_DIR + test_file_reviews
        cls.test_csv_orders = TEST_INPUT_DIR + test_file_orders
        cls.test_csv_products = TEST_INPUT_DIR + test_file_products
        cls.test_csv_sellers = TEST_INPUT_DIR + test_file_sellers
        
        # DB parameters of connection
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        dbname = os.getenv('DBNAME')
        
        
        #user="postgres"
        #password="postgres"
        #host="localhost:5433"
        #dbname="test"

        db = Database(user,password,host,dbname)
        cls.test_db = db

    def test_all_dataset_integrity_and_db_modules(self) -> None:
        """Test you can connect + use modules + all datasets integrity (DB ETL):
            0. Check that all datasets were loaded correctly (integrity check).
            1. Insert data to table
            2. Fetch data from table
            3. Fetch data from query
            4. Order queries
            5. Filter queries (and)
            6. Filter queries (or)
        """
        
        # -- DATASETS -- #

        # CUSTOMERS DATASET
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
            
        # GEOLOCATION DATASET
        result = etl.etl_geolocation(self.test_csv_geolocation)
        # Checks total columns
        self.assertEqual((len(result.columns)), 5)
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # ORDER ITEMS DATASET
        result = etl.etl_order_items(self.test_csv_items)
        # Checks total columns
        self.assertEqual((len(result.columns)), 6)
        # Checks not existence of dropped column 
        self.assertNotIn(list(result.columns), ['order_item_id'])
        self.assertEqual(result.shipping_limit_date.dtype, 'datetime64[ns]')
        # Checks Exception handle
        with self.assertRaises(Exception):
            etl.etl_order_items()
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # ORDER PAYMENTS DATASET
        result = etl.etl_order_payments(self.test_csv_payments)
        # Checks total columns
        self.assertEqual((len(result.columns)), 4)
        # Checks not existence of dropped column
        self.assertNotIn(list(result.columns), ['payment_sequential'])
        # Checks Exception handle
        with self.assertRaises(Exception):
            etl.etl_order_payments()
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # ORDER REVIEW DATASET
        result = etl.etl_order_review(self.test_csv_reviews)
        # Checks total columns 
        self.assertEqual((len(result.columns)), 6)
        # Checks not existence of dropped column
        self.assertNotIn(list(result.columns), ['review_comment_title'])
        # Checks type of converted values
        self.assertEqual(result.review_creation_date.dtype, 'datetime64[ns]')
        self.assertEqual(result.review_answer_timestamp.dtype, 'datetime64[ns]')
        # Checks Exception handle
        with self.assertRaises(Exception):
            etl.etl_order_review()
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # ORDERS DATASET
        result = etl.etl_orders(self.test_csv_orders)
        # Checks total colummns
        self.assertEqual((len(result.columns)), 8)
        # Checks type of converted values
        self.assertEqual(result.order_purchase_timestamp.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_approved_at.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_delivered_carrier_date.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_delivered_customer_date.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_estimated_delivery_date.dtype, 'datetime64[ns]')
        # Checks Exception handle
        with self.assertRaises(Exception):
            etl.etl_products()
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # PRODUCTS DATASET
        result = etl.etl_products(self.test_csv_products)
        # Checks total columns
        self.assertEqual((len(result.columns)), 9)
        # Checks type of converted values
        self.assertEqual(result.product_name_lenght.dtype, 'int64')
        self.assertEqual(result.product_description_lenght.dtype, 'int64')
        self.assertEqual(result.product_photos_qty.dtype, 'int64')
        self.assertEqual(result.product_weight_g.dtype, 'int64')
        self.assertEqual(result.product_length_cm.dtype, 'int64')
        self.assertEqual(result.product_height_cm.dtype, 'int64')
        self.assertEqual(result.product_width_cm.dtype, 'int64')
        # Checks Exception handle
        with self.assertRaises(Exception):
            etl.etl_products()
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # SELLERS DATASET
        result = etl.etl_sellers(self.test_csv_sellers)
        # Checks total columns 
        self.assertEqual((len(result.columns)), 4)
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

        # -- MODULES -- #
        dataset = pd.DataFrame({
            'id': [1, 2, 3],
            'customer': ['Juan', 'Pedro', 'Maria']
        })

        # 1. Insert data to table
        assert self.test_db.bulkInsert(dataset, "id")        
        # 2. Fetch data from table
        assert self.test_db.fetchByTable("id")
        # 3. Fetch data from query
        assert self.test_db.fetchByQuery("SELECT * FROM id")
        # 4. Order queries
        assert self.test_db.dinorderquery("id", id='ASC')
        # 5. Filter queries (and)
        assert self.test_db.dinfilterqueryand("id", id='ASC')
        # 6. Filter queries (or)
        assert self.test_db.dinfilterqueryor("id", id='ASC')

def insert_header(f):
    '''insert_header: Header to be written at the top of the testing.txt file

    Args:
        f (file): file to insert content to.

    Returns:
        file: file with header content. 
    '''
    f.write('\n')
    f.write('****************** DATABASE INTEGRATION TESTS ******************')
    f.write('\n')
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(date_time)
    f.write('\n')
    return f

def main(out = sys.stderr, verbosity = 2):
    '''main creates file with Unittest logs.

    Args:
        out: File object used by the interpreter for ins, outs and errors. Defaults to sys.stderr (errors).
        verbosity (int): Verbosity is the error level for outputting logs. Defaults to 2.
    '''
    loader = unittest.TestLoader()

    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite)
    print (f'Results logged to {os.getenv("ROOT_PATH")}/docs/txt/db-integration-tests.txt')

if __name__ == '__main__':
    with open(f'{os.getenv("ROOT_PATH")}/docs/txt/db-integration-tests.txt', 'w') as f:
        f = insert_header(f)
        main(f)