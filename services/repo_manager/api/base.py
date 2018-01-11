from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
from .redis_manager import is_redis_available, increment, get_value
import redis

base = Blueprint("base", __name__)


@base.route("/status")
def status():
    t_now = datetime.now()

    rconn = redis.Redis(
        host=current_app.config["REDIS_HOST"],
        port=current_app.config["REDIS_PORT"])

    redis_ok = is_redis_available(rconn)

    reponse = {
        "ts": t_now,
        "status": "OK" if redis_ok else "REDIS UNREACHABLE"
    }

    return jsonify(reponse)


@base.route("/counter/increment")
def counter_increment():
    t_now = datetime.now()

    rconn = redis.Redis(
        host=current_app.config["REDIS_HOST"],
        port=current_app.config["REDIS_PORT"])

    increment(rconn, "counter")

    response = {
        "ts": t_now,
        "status": get_value(rconn, "counter")
    }

    return jsonify(response)
