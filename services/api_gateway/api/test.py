from flask import Blueprint, request
from flask import jsonify
from datetime import datetime


test = Blueprint("test", __name__)


@test.route("/test", methods=["GET", "POST"])
def test_methods():
    if request.method == "GET":
        print("Received GET: ", request.args)
        response = {
            "ts": datetime.now(),
            "method": request.method,
            "args": request.args
        }
    elif request.method == "POST":
        print("Received POST: ", request.data)
        response = {
            "ts": datetime.now(),
            "method": request.method,
            "data": request.get_json()
        }
    else:
        print("Unrecognized request")
        response = {
            "ts": datetime.now(),
            "method": "UNRECOGNIZED",
            "data": None
        }

    return jsonify(response)