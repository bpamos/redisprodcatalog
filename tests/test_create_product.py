import unittest
from productcatalog.product_catalog_create import *
from productcatalog.product_catalog_update import *
from productcatalog.product_catalog_search import *

import redis

# connect redis to localhost and port
redis = redis.Redis(host='localhost', port=6379, db=0)
redis.flushdb()

def compare_arrays(array_a, array_b):
    """compare array a and array b values"""
    comparison = array_a == np.array(array_b)
    return comparison.all()


class Test_Generate_Product(unittest.TestCase):

    def test_generate_product(self):
        # example dict
        product_dict = {
            "name": 'Product_1',
            "description": 'Chicken',
            "vendor": 'WholeFoods',
            "price": 15.5,
            "currency": 'dollars',
            "category": 'Meat',
            "images": [1, 2, 3, 4, 5, 6, 7, 8]
        }

        product_obj = ProductCatalogCreate(product_dict)  # get product object
        product_obj.generate_product_catalog()

        self.assertEqual(product_obj.product_obj.productId, 'product:1', 'incorrect product id value')
        self.assertEqual(product_obj.product_obj.name, 'Product_1', 'incorrect product name value')
        self.assertEqual(product_obj.product_obj.description, 'Chicken', 'incorrect description value')
        self.assertEqual(product_obj.product_obj.vendor, 'WholeFoods', 'incorrect vendor value')
        self.assertEqual(product_obj.product_obj.price, 15.5, 'incorrect price value')
        self.assertEqual(product_obj.product_obj.currency, 'dollars', 'incorrect currency value')
        self.assertEqual(product_obj.product_obj.category, 'Meat', 'incorrect category value')
        array_a = product_obj.product_obj.images
        array_b = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(compare_arrays(array_a, array_b),True, 'incorrect image array value')

        # redis = product_obj.product_obj.redisSession[0]
        # print(redis)
        # redis.flushdb()




if __name__ == '__main__':
    unittest.main()