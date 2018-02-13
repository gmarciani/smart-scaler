from flask import jsonify
from flask import json
import inspect
from enum import Enum

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


class SimpleJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        try:
            return list(iter(obj))
        except TypeError:
            pass

        try:
            return obj.__dict__
        except AttributeError:
            pass

        return json.JSONEncoder.default(self, obj)


class AdvancedJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        #print("Processing object: ", obj)

        # if obj is a function
        if inspect.isfunction(obj):
            import_name = obj.__module__ + "." + obj.__name__
            #print("try function ", import_name)
            return import_name

        # if obj si an enumeration
        if isinstance(obj, Enum):
            #import_name = obj.__module__ + "." + obj.__class__.__name__ + "." + obj.name
            import_name = obj.name
            #print("try enumeration ", import_name)
            return import_name

        # if obj is an iterable
        try:
            #print("try iterable")
            return list(iter(obj))
        except TypeError as exc:
            pass
            #print("TypeError: ", str(exc))

        # if obj is an object
        try:
            #print("try object")
            return obj.__dict__
        except AttributeError as exc:
            pass
            #print("AttributeError: ", str(exc))

        # else
        #print("try standard")
        return json.JSONEncoder.default(self, obj)