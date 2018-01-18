import requests
import json


def get_status_service(service_host, service_port):
    """
    Get the service status.
    :param service_host: (string) the service host
    :param service_port: (integer) the service port.
    :return: (dict) the service status.
    """
    url_status_service = "http://{}:{}/status".format(service_host, service_port)

    try:
        return requests.get(url_status_service).json()
    except requests.ConnectionError or json.decoder.JSONDecodeError:
        return {"status": "UNREACHABLE"}