from services.common.util.json import MyJSONEncoder
from json import dumps


def to_json(data):
    return dumps(data, cls=MyJSONEncoder)