"""
Configurations for service RepoManager
"""


class Default:

    """
    Default configuration.
    """
    DEBUG = True

    LOG_LEVEL = "INFO"

    REDIS_HOST = "localhost"
    REDIS_PORT = 18009


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
