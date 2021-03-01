from productcatalog.calculable_object import *


class ProductCatalogSearch(CalculableObject):

    def __init__(self, data=None):
        """
        DirectionalSurvey object with a wells directional survey info
        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.data = data
        self.product_obj = ProductSearch(**self.data)

    def find_by_product_id(self):
        """

        :return:
        """
        redis = self.product_obj.redisSession[0]
        product_id = self.product_obj.productId
        return redis.hgetall(product_id)

    def find_products_in_category(self):
        """

        :return:
        """
        redis = self.product_obj.redisSession[0]
        category = f"category:{self.product_obj.category}"
        print(category)
        return redis.smembers(category)

    def find_products_by_name(self):
        """

        :return:
        """
        redis = self.product_obj.redisSession[0]
        name = self.product_obj.name

        print(name)

        product_name_id = redis.hget('product-name-index', name)
        product_name_id = product_name_id.decode("utf-8")
        return redis.hgetall(product_name_id)