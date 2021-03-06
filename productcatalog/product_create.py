from productcatalog.data_object import *


@dataclass
class ProductCreate(DataObject):
    """
    Dataclass for Product
    :parameter:
    productId:    (required) product id
    name:         (required) product name
    description:  (required) product description
    vendor:       (required) product vendor
    price:        (required) product price
    currency:     (required) currency
    category:     (required) product category
    images:       (required) images associated with product (binary value)
    :returns:
    dataclassObj: Dataclass Product object
    """
    # productId: str
    name: str
    description: str
    vendor: str
    price: float
    currency: str
    category: str
    productId: str = field(default=None, metadata={'unit': 'str'})
    images: np.ndarray = field(default=None, metadata={'unit': 'str'})
    redisSession: list = field(default=None, metadata={'unit': 'list'})

    def from_json(self):
        super().from_json()

    def redis_session(self):
        self.redisSession = [redis.Redis(host='localhost', port=6379, db=0)]

    def validate(self):
        """
        validate different parameters
        """

        #         def validate_productId(self):
        #             """
        #             validate that productId is a string
        #             :return: pass or TypeError
        #             """
        #             productId_type = type(self.productId)
        #             if productId_type is str:
        #                 pass
        #             else:
        #                 raise TypeError(f"Validation Error: productId has type {productId_type}")

        def validate_product_name(self):
            """
            validate that the product name has not been used
            :return: pass or TypeError
            """
            redis = self.redisSession[0]
            product_name = self.name
            if redis.sadd('product-names', product_name) == 1:
                pass
            else:
                raise TypeError(f"Validation Error: product name must be unique: {product_name}")

        # run validation functions
        # validate_productId(self)
        validate_product_name(self)

    def deserialize(self):
        """
        convert dict values to their proper deserialized dict values
        converts lists to np.arrays if not None
        converts value to float if not None
        converts value to str if not None
        :parameter:
        DataObject params
        :return:
        DataObject params deserialized as floats, str, int, or np.arrays
        """

        self.productId = to_type(self.productId, str)
        self.name = to_type(self.name, str)
        self.description = to_type(self.description, str)
        self.vendor = to_type(self.vendor, str)
        self.price = to_type(self.price, float)
        self.currency = to_type(self.currency, str)
        self.category = to_type(self.category, str)
        self.images = to_type(self.images, np.array)

    def __post_init__(self):
        """
        validate all data,
        serialized all validated data,
        look in all fields and types,
        if type is None pass,
        else if type given doesnt match dataclass type raise error
        """
        self.redis_session()
        self.validate()
        self.deserialize()
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                if current_type is type(None):
                    pass
                else:
                    raise ValueError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
