
import os
import sys
from dotenv import load_dotenv
from src.dbmodules import Database
import src.etl_to_db as etl
from os.path import join, dirname

scriptPath = os.path.realpath(os.path.dirname('frontend/logsetup/'))
print(scriptPath)
if scriptPath not in sys.path:
    sys.path.append(scriptPath)
import log_setup

dotenv_path = join(os.path.dirname(__file__),"config", '.env')
load_dotenv(dotenv_path)

logger = log_setup.logging.getLogger(__name__)

if __name__ == '__main__':

    logger.debug("Starting file path settings ")
    # Import env var
    customer_filepath = os.path.join(os.path.dirname(__file__), "data",
                                     "olist_customers_dataset.csv")
    geolocation_filepath = os.path.join(os.path.dirname(__file__), "data",
                                        "olist_geolocation_dataset.csv")
    order_items_filepath = os.path.join(os.path.dirname(__file__), "data",
                                        "olist_order_items_dataset.csv")
    order_payments_filepath = os.path.join(os.path.dirname(__file__), "data",
                                           "olist_order_payments_dataset.csv")
    order_review_filepath = os.path.join(os.path.dirname(__file__), "data",
                                         "olist_order_reviews_dataset.csv")
    orders_filepath = os.path.join(os.path.dirname(__file__), "data",
                                   "olist_orders_dataset.csv")
    products_filepath = os.path.join(os.path.dirname(__file__), "data",
                                     "olist_products_dataset.csv")
    sellers_filepath = os.path.join(os.path.dirname(__file__), "data",
                                    "olist_sellers_dataset.csv")
    logger.debug("End file path settings ")

    logger.debug("Starting db config settings ")
    # Import from decouple (.ini file) the connection parameters
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    dbname = os.getenv('DBNAME')
    logger.debug("End db config settings ")

    # Get dataframes for each file
    logger.debug("Starting etl processes ")
    df_customers = etl.etl_customers(customer_filepath)
    df_geolocation = etl.etl_geolocation(geolocation_filepath)
    df_order_items = etl.etl_order_items(order_items_filepath)
    df_order_payments = etl.etl_order_payments(order_payments_filepath)
    df_order_review = etl.etl_order_review(order_review_filepath)
    df_orders = etl.etl_orders(orders_filepath)
    df_products = etl.etl_products(products_filepath)
    df_sellers = etl.etl_sellers(sellers_filepath)
    logger.debug("End etl processes ")

    # Create Database object to manage database connections
    db = Database(user, password, host, dbname)
    logger.debug("Start data bulk into de db ")
    db.bulkInsert(df_customers, "customers")
    db.bulkInsert(df_sellers, "sellers")
    db.bulkInsert(df_geolocation, "geolocation")
    db.bulkInsert(df_products, "products")
    db.bulkInsert(df_orders, "orders")
    db.bulkInsert(df_order_items, "order_items")
    db.bulkInsert(df_order_payments, "order_payments")
    db.bulkInsert(df_order_review, "order_reviews")

    logger.debug("End data bulk into de db ")
