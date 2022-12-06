
import os
from src.dbmodules import Database
import src.etl_to_db as etl


if __name__ == '__main__':

    # Import env var
    customer_filepath = os.path.join(os.path.dirname(__file__), "data","olist_customers_dataset.csv")
    geolocation_filepath = os.path.join(os.path.dirname(__file__), "data","olist_geolocation_dataset.csv")
    order_items_filepath = os.path.join(os.path.dirname(__file__), "data","olist_order_items_dataset.csv")
    order_payments_filepath = os.path.join(os.path.dirname(__file__), "data","olist_order_payments_dataset.csv")
    order_review_filepath = os.path.join(os.path.dirname(__file__), "data","olist_order_reviews_dataset.csv")
    orders_filepath = os.path.join(os.path.dirname(__file__), "data","olist_orders_dataset.csv")
    products_filepath = os.path.join(os.path.dirname(__file__), "data","olist_products_dataset.csv")
    sellers_filepath = os.path.join(os.path.dirname(__file__), "data","olist_sellers_dataset.csv")
    user
    password
    host
    dbname

    # Get dataframes for each file
    df_customers = etl.etl_customers(customer_filepath)
    df_geolocation = etl.etl_geolocation(geolocation_filepath)
    df_order_items = etl.etl_order_items(order_items_filepath)
    df_order_payments = etl.etl_order_payments(order_payments_filepath)
    df_order_review = etl.etl_order_review(order_review_filepath)
    df_orders = etl.etl_orders(orders_filepath)
    df_products = etl.etl_products(products_filepath)
    df_sellers = etl.etl_sellers(sellers_filepath)

    # Create Database object to manage database connections
    db = Database(user,password,host,dbname)

    db.bulkInsert(df_customers,"customers")
    db.bulkInsert(df_geolocation,"geolocation")
    db.bulkInsert(df_order_items,"order_items")
    db.bulkInsert(df_order_payments,"order_payments")
    db.bulkInsert(df_order_review,"order_reviews")
    db.bulkInsert(df_orders,"orders")
    db.bulkInsert(df_products,"products")
    db.bulkInsert(df_sellers,"sellers")


