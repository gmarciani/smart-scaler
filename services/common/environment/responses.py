from flask import jsonify
from datetime import datetime


def output_json(data, code, headers=None):
    """
    Response layer for JSON.
    :param data: data.
    :param code: HTTP code.
    :param headers: HTTP headers
    :return: the response.
    """
    data["timestamp"] = datetime.now()
    return jsonify(data)