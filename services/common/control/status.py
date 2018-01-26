import requests
import json
from datetime import datetime
from services.common.control import connections as conn_ctrl


def get_statuses(services, config):
    """
    Get the report of services status.
    :param services: (list) list of services names.
    :param config: (dict) the current app configuration.
    :return: (dict) a dictionary {service_name: status}.
    """
    statuses = dict([(service, get_status_service(conn_ctrl.get_service_connection(service))) for service in services])

    return statuses


def get_status_service(service_conn):
    """
    Get the service status.
    :param service_conn: (SimpleConnection) the service connection.
    :return: (dict) the service status.
    """
    url = conn_ctrl.format_url("status", service_conn)

    try:
        return requests.get(url).json()
    except requests.ConnectionError or json.JSONDecodeError:
        return {"status": "UNREACHABLE"}


def compose_status_respose(statuses):
    """
    Compose the status reponse.
    :param statuses: (dict) dictionary of statuses (service_name, status)
    :return: (dict) the response.
    """
    response = {
       "ts": datetime.now(),
       "status": "OK" if all(map(lambda x: x["status"] == "OK", statuses.values())) else "FAILED",
       "services": statuses
    }

    return response


def compose_status_fake():
    """
    Compose the fake status reponse.
    :return: (dict) the response.
    """
    response = {
        "ts": datetime.now(),
        "status": "OK"
    }

    return response