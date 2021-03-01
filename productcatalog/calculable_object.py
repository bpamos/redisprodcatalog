from productcatalog.product_create import *
from productcatalog.product_update import *
from productcatalog.product_search import *

class CalculableObject(DataObject):

    def __init__(self, product_obj, **kwargs):
        """
        DirectionalSurvey object with a wells directional survey info
        Attributes:
        directional_survey_points (Dataclass Object) DataObject object
        """

        self.product_obj = product_obj

    def validate(self):
        super().validate()

    def redis_session(self):
        super.redis_session()

    def deserialize(self):
        super().deserialize()

    @classmethod
    def from_json(cls, path: PathOrStr):
        """
        Pass in a json path, either a string or a Path lib path and convert to a WellboreTrajectory data obj
        :param:
        -------
         path: PathOrStr
        :return:
        -------
        deviation_survey_obj: Obj
        :examples:
        -------
        """

        with open(path) as json_file:
            json_data = json.load(json_file)
        json_file.close()

        res = cls(data=json_data)  # converts json data
        return res

    def serialize(self):
        """
        Convert survey object to serialized json
        :parameter:
        -------
        None
        :return:
        -------
        json: str
        :examples:
        -------
        """

        self.productId = to_type(self.productId, str)
        self.name = to_type(self.name, str)
        self.description = to_type(self.description, str)
        self.vendor = to_type(self.vendor, str)
        self.price = to_type(self.price, float)
        self.currency = to_type(self.currency, str)
        self.category = to_type(self.category, str)
        self.images = to_type(self.images, np.array)

        json_obj = dict(productId=str(self.product_obj.productId),
                        name=str(self.product_obj.name),
                        description=str(self.product_obj.description),
                        vendor=str(self.product_obj.vendor),
                        price=float(self.product_obj.price),
                        currency=str(self.product_obj.currency),
                        images=list(self.product_obj.images))

        json_string = json.dumps(json_obj)  # converts a data object into a json string.

        return json_string