from flask import jsonify
from flask.json import JSONEncoder
import inspect


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


class SimpleJSONEncoder(JSONEncoder):

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


class AdvancedJSONEncoder(JSONEncoder):

    def default(self, obj):
        print("Processing object: ", obj)

        # if obj is a function
        if inspect.isfunction(obj):
            import_name = obj.__module__ + "." + obj.__name__
            print("try function ", import_name)
            return JSONEncoder.default(self, import_name)

        # if obj is an iterable
        try:
            print("try iterable")
            return list(iter(obj))
        except TypeError as exc:
            print("TypeError: ", str(exc))

        # if obj is an object
        try:
            print("try object")
            return obj.__dict__
        except AttributeError as exc:
            print("AttributeError: ", str(exc))

        # else
        print("try standard")
        return JSONEncoder.default(self, obj)