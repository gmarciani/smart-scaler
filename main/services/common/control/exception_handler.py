from flask import jsonify
from werkzeug.exceptions import HTTPException
from datetime import datetime


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
    return response, exc.code if isinstance(exc, HTTPException) else 500