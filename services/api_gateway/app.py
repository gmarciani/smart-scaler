from flask import Flask
from services.api_gateway.api.status import status as api_status
from common.control import logs as log_configurator
from services.common.control import shutdown as shutdown_ctrl
import logging


# Initialization
app = Flask(__name__)
app.config.from_object("config.Debug")

# Configure logging
log_configurator.configure(logging, app.config["LOG_LEVEL"])

# Routes
app.register_blueprint(api_status)


# Teardown Hooks
@app.teardown_appcontext
def teardown(exception):
    shutdown_ctrl.goodbye()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["API_GATEWAY_PORT"], threaded=True)
