from flask import Flask
from services.common.logs import config as log_configurator
from services.agents_manager.api.status import status as api_status
from services.agents_manager.control.scheduler import MainScheduler
from services.agents_manager.control.shutdown_hooks import simple_shutdown_hook
from services.common.control import connections as conn_ctrl
import logging
import atexit


# Initialization
app = Flask(__name__)
app.config.from_object("config.Debug")

# Configure logging
log_configurator.configure_logging(logging, app.config["LOG_LEVEL"])

# Routes
app.register_blueprint(api_status)

# Scheduled Jobs
AGENTS = {}
kubernetes_conn = conn_ctrl.get_service_connection("kubernetes", app.config)
repo_manager_conn = conn_ctrl.get_service_connection("repo_manager", app.config)
scheduler = MainScheduler(kubernetes_conn, repo_manager_conn, AGENTS, app.config["KUBERNETES_PULL"])
scheduler.start()

# Shutdown Hooks
atexit.register(simple_shutdown_hook, "My Shutdown Param")
atexit.register(lambda: scheduler.shutdown_hook())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"], threaded=True)