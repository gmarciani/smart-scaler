from services.common.util.json import SimpleJSONEncoder
from json import dumps


def to_json(data):
    return dumps(data, cls=SimpleJSONEncoder)