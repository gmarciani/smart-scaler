from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime


base = Blueprint("base", __name__)


@base.route("/status")
def status():
    t_now = datetime.now()

    res = jsonify({
        "ts": t_now,
        "status": "OK"
    })

    return res
