from productcatalog.redis_object import *


class ProductCatalogUpdate(RedisObject):

    def __init__(self, data=None):
        """
        Product Catalog Update
        Attributes:
        ProductUpdate (Dataclass Object) DataObject object
        """

        self.data = data
        self.product_obj = ProductUpdate(**self.data)


    def product_hash_update(self):
        """
        Update the Product Hash in Redis, use the product id to find the product hash,
        If any of the parameters are available update them.
        Depending on the paramenter it is a simple update, or more involved due to other data structures
        that the paramenter references.
        If name is changed it will find the original name, remove it from the secondary index hash
        and remove it from the products-names catch all set
        Then it will update those two redis data structures with the new name
        and then update the original hash

        if it is images if will update the new images by left pushing the reverse of the list of images
        into the the redis list, this is to maintain the first image as being the 'best image'
        it will push out the original images capping the list at 4 images.
        :parameter:
        -------
        :return:
        -------
        :examples:
        -------
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId
        name = self.product_obj.name
        description = self.product_obj.description
        vendor = self.product_obj.vendor
        price = self.product_obj.price
        currency = self.product_obj.currency
        category = self.product_obj.category
        images = self.product_obj.images

        # update name if not none, this involves removing and replacing a product name set value
        if name is not None:
            # get the original value of the name in the product id
            orig_name = redis.hget(product_id,'name')
            # remove it from the set product-names, (must decode bytes to string)
            orig_name = orig_name.decode("utf-8")
            redis.srem('product-names', orig_name)
            # add it the new name to the product-names set
            redis.sadd('product-names',name)

            # update the name in the product hash
            redis.hset(product_id ,'name' ,name)

            # remove and update the secondary index:
            redis.hdel('product-name-index', orig_name)
            redis.hset('product-name-index', name, product_id)

        # updates if present
        if description is not None: redis.hset(product_id ,'description' ,description)
        if vendor is not None: redis.hset(product_id ,'vendor' ,vendor)
        if price is not None: redis.hset(product_id ,'price' ,price)
        if currency is not None: redis.hset(product_id ,'currency' ,currency)

        # image updates
        if images is not None:
            list_id_images = f"{product_id}:images"
            # reverse the nparray to keep the image order, (1st in list is best image)
            for image_binary_val in images[::-1]:
                # lpush image items in
                redis.lpush(list_id_images ,str(image_binary_val))
                # ltrim the list after the 4th image
                redis.ltrim(list_id_images ,0 ,3)
                # redis.lrange(image_list_id,0,-1)

    def category_update(self):
        """
        Update Category Set in redis, find the category of the product id from the product hash
        use that category to access the category set, remove the product id from the original category set
        add the product id to the new category set
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId
        category = self.product_obj.category

        if category is not None:

            # get the original value of the category
            orig_cat = redis.hget(product_id ,'main-category')
            # remove it from the set, (must decode bytes to string)
            orig_cat = orig_cat.decode("utf-8")
            orig_cat_id = f"category:{orig_cat}"
            redis.srem(orig_cat_id, product_id)

            # update in the product hash
            redis.hset(product_id ,'main-category' ,category)

            # add it to the new set
            category_id = f"category:{category}"
            redis.sadd(category_id ,product_id)



    def product_hash_delete(self):
        """
        Delete Product Hash by product Id in redis
        :parameter:
        -------
        :return:
        -------
        :examples:
        -------
        """
        redis = self.product_obj.redisSession[0]
        # get md, inc, and azim arrays
        product_id = self.product_obj.productId


        # get the original value of the name in the product id
        orig_name = redis.hget(product_id ,'name')
        # remove it from the set product-names, (must decode bytes to string)
        orig_name = orig_name.decode("utf-8")
        redis.srem('product-names', orig_name)

        # remove from the secondary index hash:
        redis.hdel('product-name-index', orig_name)

        # delete the hash
        redis.delete(product_id)

    def images_list_delete(self):
        """
        delete image list in redis
        :return:
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId
        # images = self.product_obj.images

        list_id_images = f"{product_id}:images"
        redis.delete(list_id_images)


    def category_remove(self):
        """
        Remove product id from category set in redis
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId

        # get the original value of the category
        orig_cat = redis.hget(product_id ,'main-category')
        # remove it from the set, (must decode bytes to string)
        orig_cat = orig_cat.decode("utf-8")
        orig_cat_id = f"category:{orig_cat}"
        redis.srem(orig_cat_id, product_id)

    def update_product(self):
        """
        Run through product update methods

        :return:
        """

        self.product_hash_update()  # get product hash

        self.category_update() # get category set

    def delete_product(self):
        """
        Run through product delete methods

        :return:
        """

        self.category_remove()
        self.product_hash_delete()
        self.images_list_delete()