from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
import requests


base = Blueprint("base", __name__)


@base.route("/status")
def status():
    t_now = datetime.now()

    url_status_agents_manager = "http://{}:{}/status".format(current_app.config["AGENTS_MANAGER_HOST"],
                                                             current_app.config["AGENTS_MANAGER_PORT"])

    url_status_repo_manager = "http://{}:{}/status".format(current_app.config["REPO_MANAGER_HOST"],
                                                             current_app.config["REPO_MANAGER_PORT"])

    try:
        status_agents_manager = requests.get(url_status_agents_manager, timeout=5).json()
    except:
        status_agents_manager = None

    try:
        status_repo_manager = requests.get(url_status_repo_manager, timeout=5).json()
    except:
        status_repo_manager = None

    agents_manager_ok = (status_agents_manager is not None and status_agents_manager["status"] == "OK")
    repo_manager_ok = (status_repo_manager is not None and status_repo_manager["status"] == "OK")

    status_overall = "OK" if agents_manager_ok and repo_manager_ok else "FAILED"

    res = jsonify({
        "ts": t_now,
        "status": status_overall,
        "status_agents_manager": status_agents_manager if status_agents_manager is not None else "UNREACHEABLE",
        "status_repo_manager": status_repo_manager if status_repo_manager is not None else "UNREACHEABLE"
    })

    return res


if __name__ == "__main__":

    PROXIES = {
        "http": "http://10.237.220.72:80",
        "https": "http://10.237.220.72:80"
    }

    status_agents_manager = requests.get("http://127.0.0.1:18002/status", proxies=PROXIES)

    print("status_agents_manager: {}".format(status_agents_manager))