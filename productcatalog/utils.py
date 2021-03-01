from .imports import *

# Utils

def if_none(a: Any, b: Any) -> Any:
    "`a` if `a` is not None, otherwise `b`."
    return b if a is None else a


def to_type(a: Any, data_type):
    """
    If item is None, return None, else, convert to an data_type specified
    (ie. np.array, str, int, float, ect..)
    :parameter: a (Any or None)
    :returns: None or data_type(a)
    """
    return None if a is None else data_type(a)

def redis_session(host='localhost', port=6379, db=0):
    print('hi')
    return redis.Redis(host=host, port=port, db=db)