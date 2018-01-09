from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
import redis

base = Blueprint("base", __name__)


@base.route("/status")
def status():
    t_now = datetime.now()

    rconn = redis.Redis(
        host=current_app.config["REDIS_HOST"],
        port=current_app.config["REDIS_PORT"],
        password=current_app.config["REDIS_PASSWORD"])

    redis_ok = is_redis_available(rconn)

    res_status = {
        "ts": t_now,
        "status": "OK" if redis_ok else "REDIS UNREACHABLE"
    }

    response = jsonify(res_status)

    return response


def is_redis_available(rconn):
    try:
        rconn.get(None)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True
