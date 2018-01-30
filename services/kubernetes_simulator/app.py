from flask import Flask
from services.kubernetes_simulator.api.status import status as api_status
from services.kubernetes_simulator.api.pods import pods as api_pods
from services.kubernetes_simulator.api.smart_scalers import smart_scalers as api_smart_scalers
from services.common.logs import config as log_configurator
from services.agents_manager.control.shutdown_hooks import simple_shutdown_hook
import logging
import atexit


# Initialization
app = Flask(__name__)
app.config.from_object("config.Debug")

# Configure logging
log_configurator.configure_logging(logging, app.config["LOG_LEVEL"])

# Routes
app.register_blueprint(api_status)
app.register_blueprint(api_pods)
app.register_blueprint(api_smart_scalers)

# Shutdown Hooks
atexit.register(simple_shutdown_hook, "My Shutdown Param")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["KUBERNETES_PORT"], threaded=True)
