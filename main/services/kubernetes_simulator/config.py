"""
Configurations for service KubernetesSimulator
"""


class Default:
    """
    Default configuration.
    """
    DEBUG = True

    LOG_LEVEL = "INFO"

    KUBERNETES_HOST = "localhost"
    KUBERNETES_PORT = 18008


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