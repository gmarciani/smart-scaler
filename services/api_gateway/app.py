from services.common.environment.webapp import WebApp as App
from services.common.control import shutdown as shutdown_ctrl
from services.api_gateway.config import Debug as AppConfig
from services.api_gateway.api.status import Status


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Shutdown
app.add_shutdown_hook(shutdown_ctrl.goodbye)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["API_GATEWAY_PORT"], threaded=True)