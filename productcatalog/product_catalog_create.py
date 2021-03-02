from productcatalog.redis_object import *
#from .imports import *


class ProductCatalogCreate(RedisObject):

    def __init__(self, data=None):
        """
        Product Catalog Create
        Attributes:
        Product_create (Dataclass Object) DataObject object
        """

        self.data = data
        self.product_obj = ProductCreate(**self.data)

    def product_id_gen(self):
        "Generate the product Id, it is a incremental value"
        redis = self.product_obj.redisSession[0]
        product_id_incr = redis.incr('product_id_incr', 1)
        product_id = f"product:{product_id_incr}"

        self.product_obj.productId = product_id

    def product_hash(self):
        """
        Create product hash in redis
        Fill in the hash with the parameter values
        Since redis does not have nested data strucutures you must create a new index for images
        because images is mulitple items in a list.
        Create a list and Rpush the images into the list, this will ensure the the 1st image
        in the list is the first image, cap the list at 4 images.
        :parameter:
        -------
        None
        :return:
        -------
        :examples:
        -------
        """
        redis = self.product_obj.redisSession[0]
        # get md, inc, and azim arrays
        product_id = self.product_obj.productId
        name = self.product_obj.name
        description = self.product_obj.description
        vendor = self.product_obj.vendor
        price = self.product_obj.price
        currency = self.product_obj.currency
        category = self.product_obj.category
        images = self.product_obj.images

        redis.hset(product_id, 'name', name)
        redis.hset(product_id, 'description', description)
        redis.hset(product_id, 'vendor', vendor)
        redis.hset(product_id, 'price', price)
        redis.hset(product_id, 'currency', currency)
        redis.hset(product_id, 'category', category)

        # create a list of images, keep only 4 per product
        # first image in the list is the number 1 image
        list_id_images = f"{product_id}:images"
        for image_binary_val in images:
            redis.rpush(list_id_images, str(image_binary_val))
            redis.ltrim(list_id_images, 0, 3)
            # redis.lrange(image_list_id,0,-1)

    def product_name_secondary_index(self):
        """"
        Create Secondary Index in redis
        Create a hash named 'product-name-index' then put the name of the product as the Key
        and product Id as the value, so you can quickly access it by name and get the product Id
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId
        name = self.product_obj.name

        redis.hset('product-name-index', name, product_id)

    def category_set(self):
        """
        Create category set in redis
        """
        redis = self.product_obj.redisSession[0]

        product_id = self.product_obj.productId
        category = self.product_obj.category

        category_id = f"category:{category}"
        redis.sadd(category_id, product_id)

    def generate_product_catalog(self):
        """
        Run through product create methods

        :return:
        """
        self.product_id_gen()  # get generated product id

        self.product_hash()  # get product hash

        self.product_name_secondary_index() # get product name secondary index

        self.category_set()  # get category set