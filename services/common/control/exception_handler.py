from flask import jsonify
from datetime import datetime
from services.common.model.exception import RESTException


def handle_exception(exc):
    """
    Handle all exceptions.
    :param exc: (Exception) the exception.
    :return: (code, response)
    """
    response = jsonify({
        "ts": datetime.now(),
        "error": str(exc)
    })
    return response, exc.code if isinstance(exc, RESTException) else 500