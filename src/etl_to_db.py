import pandas as pd
import os
import sys

# change to the script path
scriptPath = os.path.realpath(os.path.dirname('frontend/logsetup/'))
os.chdir(scriptPath)

# append the relative location to import setup logs
sys.path.append("./logsetup")

import log_setup


logger = log_setup.logging.getLogger(__name__)
logger_r = log_setup.logging.getLogger('db')


def etl_customers(filepath: str) -> object:
    """etl_customers ETL to process customers csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    try:
        df_customers = pd.read_csv(filepath)
        logger_r.debug(f"File {filepath} open succesfully ")
        df_customers.drop('customer_unique_id', axis=1, inplace=True)
        return df_customers
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")
    except Exception as a:
        logger_r.debug(f"File {filepath} format its not what was expected {a}")
        logger.error(f"File {filepath} format its not what was expected  {a}")             


def etl_geolocation(filepath: str) -> object:
    """etl_customers ETL to process geolocation csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    try:
        df_geolocation = pd.read_csv(filepath)
        logger_r.debug(f"File {filepath} open succesfully ")
        return df_geolocation
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")        


def etl_order_items(filepath: str) -> object:
    """etl_customers ETL to process Order Items csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    try:
        df_order_items = pd.read_csv(filepath)
        logger_r.debug(f"File {filepath} open succesfully ")
        df_order_items.drop('order_item_id', axis=1, inplace=True)
        df_order_items['shipping_limit_date'] = pd.to_datetime(df_order_items[
            'shipping_limit_date'], infer_datetime_format=True)
        return df_order_items
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")        
    except Exception as a:
        logger_r.debug(f"File {filepath} format its not what was expected {a}")
        logger.error(f"File {filepath} format its not what was expected  {a}")             


def etl_order_payments(filepath: str) -> object:
    """etl_customers ETL to process order payments csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    try:
        df_order_payments = pd.read_csv(filepath)
        df_order_payments.drop('payment_sequential', axis=1, inplace=True)
        logger_r.debug(f"File {filepath} open succesfully ")
        return df_order_payments
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")        
    except Exception as a:
        logger_r.debug(f"File {filepath} format its not what was expected {a}")
        logger.error(f"File {filepath} format its not what was expected  {a}")    


def etl_order_review(filepath: str) -> object:
    """etl_customers ETL to process order review csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    try:
        df_order_reviews = pd.read_csv(filepath)
        df_order_reviews.drop('review_comment_title', axis=1, inplace=True)
        df_order_reviews['review_creation_date'] = pd.to_datetime(
            df_order_reviews['review_creation_date'], format='%Y-%m-%d %H:%M:%S')
        df_order_reviews['review_answer_timestamp'] = pd.to_datetime(
            df_order_reviews['review_answer_timestamp'],
            infer_datetime_format=True)
        logger_r.debug(f"File {filepath} open succesfully ")
        return df_order_reviews
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")        
    except Exception as a:
        logger_r.debug(f"File {filepath} format its not what was expected {a}")
        logger.error(f"File {filepath} format its not what was expected  {a}")    

def etl_orders(filepath: str) -> object:
    """etl_customers ETL to process orders csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    try:
        df_orders = pd.read_csv(filepath)
        df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders[
            'order_purchase_timestamp'], format='%Y-%m-%d %H:%M:%S')
        df_orders['order_approved_at'] = pd.to_datetime(df_orders[
            'order_approved_at'], format='%Y-%m-%d %H:%M:%S')
        df_orders['order_delivered_carrier_date'] = pd.to_datetime(df_orders[
            'order_delivered_carrier_date'], format='%Y-%m-%d %H:%M:%S')
        df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders[
            'order_delivered_customer_date'], format='%Y-%m-%d %H:%M:%S')
        df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders[
            'order_estimated_delivery_date'], format='%Y-%m-%d %H:%M:%S')
        logger_r.debug(f"File {filepath} open succesfully ")
        return df_orders
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")        
    except Exception as a:
        logger_r.debug(f"File {filepath} format its not what was expected {a}")
        logger.error(f"File {filepath} format its not what was expected  {a}")    


def etl_products(filepath: str) -> object:
    """etl_customers ETL to process products csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    try:
        df_products = pd.read_csv(filepath)
        df_products.fillna('-1', inplace=True)
        df_products['product_name_lenght'] = df_products[
            'product_name_lenght'].astype('int64')
        df_products['product_description_lenght'] = df_products[
            'product_description_lenght'].astype('int64')
        df_products['product_photos_qty'] = df_products[
            'product_photos_qty'].astype('int64')
        df_products['product_weight_g'] = df_products[
            'product_weight_g'].astype('int64')
        df_products['product_length_cm'] = df_products[
            'product_length_cm'].astype('int64')
        df_products['product_height_cm'] = df_products[
            'product_height_cm'].astype('int64')
        df_products['product_width_cm'] = df_products[
            'product_width_cm'].astype('int64')
        logger_r.debug(f"File {filepath} open succesfully ")
        return df_products
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ")        
    except Exception as a:
        logger_r.debug(f"File {filepath} format its not what was expected {a}")
        logger.error(f"File {filepath} format its not what was expected  {a}")    


def etl_sellers(filepath: str) -> object:
    """etl_customers ETL to process sellers csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    try:
        df_order_sellers = pd.read_csv(filepath)
        logger_r.debug(f"File {filepath} open succesfully ")
        return df_order_sellers
    except IOError:
        logger_r.debug(f"File {filepath} cant be opened ")
        logger.error(f"File {filepath} cant be opened ") 