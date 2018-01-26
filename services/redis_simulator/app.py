from flask import Flask
from services.redis_simulator.api.status import status
from services.redis_simulator.api.database import database
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
app.register_blueprint(status)
app.register_blueprint(database)

# Shutdown Hooks
atexit.register(simple_shutdown_hook, "My Shutdown Param")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REDIS_PORT"], threaded=True)
