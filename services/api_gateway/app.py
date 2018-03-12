"""
The Flask application that realizes the service 'API Gateway'.
"""


from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.api_gateway.config import Debug as AppConfig
from services.api_gateway.api.status import Status
from sys import argv


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    if len(argv) > 1:
        app.config["API_GATEWAY_PORT"] = int(argv[1])
    app.start(port=app.config["API_GATEWAY_PORT"])