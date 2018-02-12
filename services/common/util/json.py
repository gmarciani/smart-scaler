from flask import jsonify
from flask.json import JSONEncoder

from services.common.model.resources.pod import PodResource


def output_json(data, code, headers=None):
    """
    Response layer for JSON.
    :param data: data.
    :param code: HTTP code.
    :param headers: HTTP headers
    :return: the response.
    """
    #data["timestamp"] = datetime.now()
    return jsonify(data)


class MyJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            return list(iter(obj))
        except TypeError:
            pass

        try:
            return obj.__dict__
        except AttributeError:
            pass

        return JSONEncoder.default(self, obj)