import os
import sys
import unittest

import pandas as pd

# Declare root path: pulled from ENV file.
sys.path.append(".")
from src import etl_to_db as etl




class TestETL(unittest.TestCase):

    def setUp(self) -> None:
        """ Load data setUp """
        TEST_INPUT_DIR = f'{os.getenv("ROOT_PATH")}/tests/data_input/'
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

    def test_etl_customers(self) -> None:
        """Test ETL customers transformations.
        """
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
            
    def test_etl_geolocation(self) -> None:
        """Test ETL geolocation transformations.
        """
        result = etl.etl_geolocation(self.test_csv_geolocation)

        # Checks total columns
        self.assertEqual((len(result.columns)), 5)
     
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))

    def test_etl_order_items(self) -> None:
        """Test ETL order items transformations.
        """
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

    def test_etl_order_payments(self) -> None:
        """Test ETL order payments transformations.
        """
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

    def test_etl_order_review(self) -> None:
        """Test ETL orders reviews transformations.
        """
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
        

    def test_etl_orders(self) -> None:
        """Test ETL orders transformations.
        """
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

    def test_etl_products(self) -> None:
        """Test ETL products transformations.
        """
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

    def test_etl_sellers(self) -> None:
        """Test ETL sellers transformations.
        """
        result = etl.etl_sellers(self.test_csv_sellers)

        # Checks total columns 
        self.assertEqual((len(result.columns)), 4)
        
        # Checks returns a dataframe 
        self.assertEqual(type(result), type(pd.DataFrame()))


if __name__ == '__main__':
    unittest.main()

