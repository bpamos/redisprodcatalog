from productcatalog.calculable_object import *


class ProductCatalogUpdate(CalculableObject):

    def __init__(self, data=None):
        """
        DirectionalSurvey object with a wells directional survey info
        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.data = data
        self.product_obj = ProductUpdate(**self.data)


    def product_hash_update(self):
        """
        Calculate TVD, n_s_deviation, e_w_deviation, and dls values along the wellbore
        using md, inc, and azim arrays
        :parameter:
        -------
        None
        :return:
        -------
        calculated np.array values
        tvd: np.array
        dls: np.array
        e_w_deviation: np.array
        n_s_deviation: np.array
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
        You can get the ID from the product hash and create the cateogry hash
        you will call the current main cat product id. Find out what it is, then create a unique ID for it.
        Like, MEAT, and then update the set??? idk. ughh
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
        Calculate TVD, n_s_deviation, e_w_deviation, and dls values along the wellbore
        using md, inc, and azim arrays
        :parameter:
        -------
        None
        :return:
        -------
        calculated np.array values
        tvd: np.array
        dls: np.array
        e_w_deviation: np.array
        n_s_deviation: np.array
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

        :return:
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId
        # images = self.product_obj.images

        list_id_images = f"{product_id}:images"
        redis.delete(list_id_images)


    def category_remove(self):
        """
        You can get the ID from the product hash and create the cateogry hash
        you will call the current main cat product id. Find out what it is, then create a unique ID for it.
        Like, MEAT, and then update the set??? idk. ughh
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

        self.product_hash_update()  # get product hash

        self.category_update() # get category set

    def delete_product(self):

        self.category_remove()
        self.product_hash_delete()
        self.images_list_delete()