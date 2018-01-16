"""
Default configuration for service AgentsManager
"""


class Default:
    DEBUG = True

    API_GATEWAY_HOST = "localhost"
    API_GATEWAY_PORT = 18001

    AGENTS_MANAGER_HOST = "localhost"
    AGENTS_MANAGER_PORT = 18002

    REPO_MANAGER_HOST = "localhost"
    REPO_MANAGER_PORT = 18003

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379

    KUBERNETES_HOST = "localhost"
    KUBERNETES_PORT = 18008
    KUBERNETES_PULL = 10  # seconds
