import sys
import unittest

sys.path.append('')

import src.etl_to_db as etl


class TestCalculator(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_etl_customers(self) -> None:
        result = etl.etl_customers()

        # Checks total columns 
        self.assertEqual((len(result.columns)), 4)

        # Checks not existence of dropped column
        self.assertNotIn(list(result.columns), ['customer_unique_id'])

    def test_etl_geolocation(self) -> None:
        result = etl.etl_geolocation()

        # Checks total columns
        self.assertEqual((len(result.columns)), 5)

    def test_etl_order_items(self) -> None:
        result = etl.etl_order_items()

        # Checks total columns
        self.assertEqual((len(result.columns)), 6)

        # Checks not existence of dropped column 
        self.assertNotIn(list(result.columns), ['order_item_id'])
        self.assertEqual(result.shipping_limit_date.dtype, 'datetime64[ns]')

    def test_etl_order_payments(self) -> None:
        result = etl.etl_order_payments()

        # Checks total columns
        self.assertEqual((len(result.columns)), 4)

        # Checks not existence of dropped column
        self.assertNotIn(list(result.columns), ['payment_sequential'])

    def test_etl_order_review(self) -> None:
        result = etl.etl_order_review()

        # Checks total columns 
        self.assertEqual((len(result.columns)), 6)

        # Checks not existence of dropped column
        self.assertNotIn(list(result.columns), ['review_comment_title'])

        # Checks type of converted values
        self.assertEqual(result.review_creation_date.dtype, 'datetime64[ns]')
        self.assertEqual(result.review_answer_timestamp.dtype, 'datetime64[ns]')

    def test_etl_orders(self) -> None:
        result = etl.etl_orders()

        # Checks total colummns
        self.assertEqual((len(result.columns)), 8)

        # Checks type of converted values
        self.assertEqual(result.order_purchase_timestamp.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_approved_at.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_delivered_carrier_date.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_delivered_customer_date.dtype, 'datetime64[ns]')
        self.assertEqual(result.order_estimated_delivery_date.dtype, 'datetime64[ns]')

    def test_etl_products(self) -> None:
        result = etl.etl_products()

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

    def test_etl_sellers(self) -> None:
        result = etl.etl_sellers()

        # Checks total columns 
        self.assertEqual((len(result.columns)), 4)


if __name__ == '__main__':
    unittest.main()

