from flask import current_app, g
from common.model.connection import SimpleConnection


SERVICES = ["api_gateway", "agents_manager", "repo_manager", "redis", "kubernetes"]


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


def get_service_connection(service_name, app_config=None):
    """
    Get the connection to the specified service.
    :param service_name: (string) the service name.
    :param app_config: (dict) the Flask app configuration.
    :return: (SimpleConnection) the connection to the service.
    """
    if app_config is not None:
        host = app_config[SERVICES_MAP[service_name]["config_host"]]
        port = app_config[SERVICES_MAP[service_name]["config_port"]]
        return SimpleConnection(host, port)
    else:
        attr_name = SERVICES_MAP[service_name]["attr_name"]
        if not hasattr(g, attr_name):
            host = current_app.config[SERVICES_MAP[service_name]["config_host"]]
            port = current_app.config[SERVICES_MAP[service_name]["config_port"]]
            conn = SimpleConnection(host, port)
            setattr(g, attr_name, conn)
        return getattr(g, attr_name)


def open_repository_connection():
    """
    Open the connection to the repository.
    :return: (SimpleConnection) the connection to the repository.
    """
    if not hasattr(g, "repository_conn"):
        g.repository_conn = SimpleConnection(current_app.config["REDIS_HOST"], current_app.config["REDIS_PORT"])
    return g.repository_conn


def close_repository_connection():
    """
    Close the connection to the repository.
    :return: (void)
    """
    if hasattr(g, "repo_conn"):
        g.repository_conn = None