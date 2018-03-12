"""
Configurations for the service 'API Gateway'.
"""


class Default:
    """
    Default configuration.
    """
    DEBUG = True

    LOG_LEVEL = "INFO"

    API_GATEWAY_HOST = "localhost"
    API_GATEWAY_PORT = 18002

    AGENT_HOST = "localhost"
    AGENT_PORT = 18003

    KUBERNETES_HOST = "localhost"
    KUBERNETES_PORT = 18001
    KUBERNETES_PULL = 20  # seconds

    REPOSITORY_HOST = "172.17.0.2"
    REPOSITORY_PORT = 6379

class Debug(Default):
    """
    Debug configuration.
    """
    DEBUG = True

    LOG_LEVEL = "DEBUG"


class Production(Default):
    """
    Production configuration.
    """
    DEBUG = False
