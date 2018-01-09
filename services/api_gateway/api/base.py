from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
import requests


base = Blueprint("base", __name__)


@base.route("/status")
def status():
    t_now = datetime.now()

    status_agents_manager = get_status_agents_manager()
    status_repo_manager = get_status_repo_manager()

    agents_manager_ok = (status_agents_manager is not None and status_agents_manager["status"] == "OK")
    repo_manager_ok = (status_repo_manager is not None and status_repo_manager["status"] == "OK")
    overall_ok = (agents_manager_ok and repo_manager_ok)

    overall_status = {
        "ts": t_now,
        "status": "OK" if overall_ok else "FAILED",
        "status_agents_manager": status_agents_manager if status_agents_manager is not None else "UNREACHEABLE",
        "status_repo_manager": status_repo_manager if status_repo_manager is not None else "UNREACHEABLE"
    }

    response = jsonify(overall_status)

    return response


def get_status_agents_manager():
    url_status_agents_manager = "http://{}:{}/status".format(current_app.config["AGENTS_MANAGER_HOST"],
                                                             current_app.config["AGENTS_MANAGER_PORT"])
    try:
        status_agents_manager = requests.get(url_status_agents_manager, timeout=5).json()
    except requests.ConnectionError:
        status_agents_manager = None

    return status_agents_manager


def get_status_repo_manager():
    url_status_repo_manager = "http://{}:{}/status".format(current_app.config["REPO_MANAGER_HOST"],
                                                             current_app.config["REPO_MANAGER_PORT"])
    try:
        status_repo_manager = requests.get(url_status_repo_manager, timeout=5).json()
    except requests.ConnectionError:
        status_repo_manager = None

    return status_repo_manager