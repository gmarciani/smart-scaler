from flask import current_app
from services.common.model.connection import SimpleConnection


SERVICES = ["api_gateway", "agents_manager", "repository", "kubernetes"]


def _build_services_map(services):
    """
    Build the services map, used to retrieve connections.
    :param services: (list) the list of service names.
    :return: (dict) the services map.
    """
    services_map = {}

    for service_name in services:
        services_map[service_name] = {
            "attr_name": "{}_conn".format(service_name.lower()),
            "config_host": "{}_HOST".format(service_name.upper()),
            "config_port": "{}_PORT".format(service_name.upper()),
        }

    return services_map


SERVICES_MAP = _build_services_map(SERVICES)


def format_url(rest_interface, connection, protocol="http"):
    """
    Create a URL.
    :param rest_interface: (string) the REST interface name.
    :param connection: (SimpleConnection) the connection.
    :param protocol: (string) the protocol name (default is 'http').
    :return: (string) the URL.
    """
    return "{}://{}:{}/{}".format(protocol, connection.host, connection.port, rest_interface)


def get_service_connection(service_name):
    """
    Get the connection to the specified service.
    :param service_name: (string) the service name.
    :return: (SimpleConnection) the connection to the service.
    """
    attr_name = SERVICES_MAP[service_name]["attr_name"]

    try:
        conn = SERVICES_MAP[service_name][attr_name]
    except KeyError:
        host = current_app.config[SERVICES_MAP[service_name]["config_host"]]
        port = current_app.config[SERVICES_MAP[service_name]["config_port"]]
        conn = SimpleConnection(host, port)
        SERVICES_MAP[service_name][attr_name] = conn
    return conn