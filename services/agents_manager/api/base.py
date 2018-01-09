from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime


base = Blueprint("base", __name__)


@base.route("/status")
def status():

    res_status = {
        "ts": datetime.now(),
        "status": "OK"
    }

    response = jsonify(res_status)

    return response
