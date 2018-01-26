from flask import Flask
from services.repo_manager.api.status import status
from services.repo_manager.api.repo import repo
from services.repo_manager.api.learning_contexts import learning_contexts
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
app.register_blueprint(repo)
app.register_blueprint(learning_contexts)

# Shutdown Hooks
atexit.register(simple_shutdown_hook, "My Shutdown Param")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REPO_MANAGER_PORT"], threaded=True)
