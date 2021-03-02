import unittest
from productcatalog.product_catalog_create import *
from productcatalog.product_catalog_update import *
from productcatalog.product_catalog_search import *

#current_dir = Path.cwd()
#path = current_dir.parent
#json_path = path / 'data/wellbore_survey.json'

# import redis
import redis

# connect redis to localhost and port
redis = redis.Redis(host='localhost', port=6379, db=0)
redis.flushdb()

def compare_arrays(array_a, array_b):
    """compare array a and array b values"""
    comparison = array_a == np.array(array_b)
    return comparison.all()


class Test_Find_Product_By_Id(unittest.TestCase):

    def test_find_product_by_id(self):
        import redis
        redis = redis.Redis(host='localhost', port=6379, db=0)
        redis.flushdb()
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

        # product find
        product_dict = {
            "productId": 'product:1'
        }

        product_obj = ProductCatalogSearch(product_dict)  # get product object
        value = product_obj.find_by_product_id()

        redis_value = {b'name': b'Product_1',
                       b'description': b'Chicken',
                       b'vendor': b'WholeFoods',
                       b'price': b'15.5',
                       b'currency': b'dollars',
                       b'category': b'Meat'}

        self.assertEqual(value, redis_value, 'incorrect product id value')

        # flushdb
        redis = product_obj.product_obj.redisSession[0]
        print(redis)
        redis.flushdb()

    def test_find_images_by_id(self):
        import redis
        redis = redis.Redis(host='localhost', port=6379, db=0)
        redis.flushdb()
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

        # product images find
        product_dict = {
            "productId": 'product:1'
        }

        product_obj = ProductCatalogSearch(product_dict)  # get product object
        value = product_obj.find_images_by_product_id()
        print(value)
        redis_value = [b'1', b'2', b'3', b'4']
        print(redis_value)
        self.assertEqual(value, redis_value, 'incorrect product id value')


if __name__ == '__main__':
    unittest.main()