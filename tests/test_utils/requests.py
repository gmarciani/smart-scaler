from services.common.util.jsonutil import AdvancedJSONEncoder as JSONEncoder
from json import dumps


def to_json(data):
    return dumps(data, cls=JSONEncoder)