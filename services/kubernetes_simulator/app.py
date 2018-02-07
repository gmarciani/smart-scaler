from flask import Flask
from services.kubernetes_simulator.api.status import status as api_status
from services.kubernetes_simulator.api.pods import pods as api_pods
from services.kubernetes_simulator.api.smart_scalers import smart_scalers as api_smart_scalers
from common.control import logs as log_configurator
from services.kubernetes_simulator.control import registry as registry_ctrl
from services.common.control import shutdown as shutdown_ctrl
import logging


# Initialization
app = Flask(__name__)
app.config.from_object("config.Debug")

# Configure logging
log_configurator.configure(logging, app.config["LOG_LEVEL"])

# Routes
app.register_blueprint(api_status)
app.register_blueprint(api_pods)
app.register_blueprint(api_smart_scalers)


# Teardown Hooks
@app.teardown_appcontext
def teardown(exception):
    registry_ctrl.teardown_registry()
    shutdown_ctrl.goodbye()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["KUBERNETES_PORT"], threaded=True)
