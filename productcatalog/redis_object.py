from productcatalog.product_create import *
from productcatalog.product_update import *
from productcatalog.product_search import *

class RedisObject(DataObject):

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