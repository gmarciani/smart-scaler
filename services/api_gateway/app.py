import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.api_gateway.config import Debug as AppConfig
from services.api_gateway.api.status import Status


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    app.start(port=app.config["API_GATEWAY_PORT"])