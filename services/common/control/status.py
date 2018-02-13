import requests
import json
from services.common.control import connections as conn_ctrl


def get_statuses(services):
    """
    Get the report of services status.
    :param services: (list) list of services names.
    :return: (dict) a dictionary {service_name: status}.
    """
    return dict([(service, get_status_service(conn_ctrl.get_service_connection(service))) for service in services])


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
        return dict(status="UNREACHABLE")


def compose_status_respose(statuses):
    """
    Compose the status reponse.
    :param statuses: (dict) dictionary of statuses (service_name, status)
    :return: (dict) the response.
    """
    return dict(
        status="OK" if all(map(lambda x: x["status"] == "OK", statuses.values())) else "FAILED",
        services=statuses)


def compose_status_fake():
    """
    Compose the fake status reponse.
    :return: (dict) the response.
    """
    return dict(status="OK")