from productcatalog.utils import *


class DataObject(metaclass=abc.ABCMeta):
    """
    A abstract base class to work with subclasses `DeviationSurvey` and `CalculableObject`.
    """

    @abstractmethod
    def from_json(self):
        pass

    @abstractmethod
    def redis_session(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass
