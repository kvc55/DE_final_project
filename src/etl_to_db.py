import pandas as pd


def etl_customers(filepath: str) -> object:
    """etl_customers ETL to process customers csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """
    df_customers = pd.read_csv(filepath)
    df_customers.drop('customer_unique_id', axis=1, inplace=True)
    return df_customers


def etl_geolocation(filepath: str) -> object:
    """etl_customers ETL to process geolocation csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    df_geolocation = pd.read_csv(filepath)
    return df_geolocation


def etl_order_items(filepath: str) -> object:
    """etl_customers ETL to process Order Items csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    df_order_items = pd.read_csv(filepath)
    df_order_items.drop('order_item_id', axis=1, inplace=True)
    df_order_items['shipping_limit_date'] = pd.to_datetime(df_order_items[
        'shipping_limit_date'], infer_datetime_format=True)
    return df_order_items


def etl_order_payments(filepath: str) -> object:
    """etl_customers ETL to process order payments csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    df_order_payments = pd.read_csv(filepath)
    df_order_payments.drop('payment_sequential', axis=1, inplace=True)

    return df_order_payments


def etl_order_review(filepath: str) -> object:
    """etl_customers ETL to process order review csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    df_order_reviews = pd.read_csv(filepath)
    df_order_reviews.drop('review_comment_title', axis=1, inplace=True)
    df_order_reviews['review_creation_date'] = pd.to_datetime(
        df_order_reviews['review_creation_date'], format='%Y-%m-%d %H:%M:%S')
    df_order_reviews['review_answer_timestamp'] = pd.to_datetime(
        df_order_reviews['review_answer_timestamp'],
        infer_datetime_format=True)
    return df_order_reviews


def etl_orders(filepath: str) -> object:
    """etl_customers ETL to process orders csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

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
    return df_orders


def etl_products(filepath: str) -> object:
    """etl_customers ETL to process products csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    df_products = pd.read_csv(filepath)
    df_products.dropna(inplace=True)
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

    return df_products


def etl_sellers(filepath: str) -> object:
    """etl_customers ETL to process sellers csv

    :param filepath: location/filename.csv of the file to process
    :type filepath: str
    :return: processed Dataframe
    :rtype: object
    """

    df_order_sellers = pd.read_csv(filepath)
    return df_order_sellers
