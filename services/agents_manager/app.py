from flask import Flask
from api_agents_manager.status import status
from control_agents_manager.scheduler import MainScheduler
from control_agents_manager.jobs import shutdown_hook
import atexit
import logging


# Initialization
app = Flask(__name__)
app.config.from_object("config.Debug")

# Configure logger
logging.basicConfig(level=logging._nameToLevel[app.config["LOG_LEVEL"]])
logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.FATAL)

# Routes
app.register_blueprint(status)

# Scheduled Jobs
AGENTS = {}
kubernetes_conn = (app.config["KUBERNETES_HOST"], app.config["KUBERNETES_PORT"])
repo_manager_conn = (app.config["REPO_MANAGER_HOST"], app.config["REPO_MANAGER_PORT"])
scheduler = MainScheduler(kubernetes_conn, repo_manager_conn, AGENTS, app.config["KUBERNETES_PULL"])
scheduler.start()

# Shutdown Hooks
atexit.register(shutdown_hook, "My Shutdown Param")
atexit.register(lambda: scheduler.shutdown_hook())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"], threaded=True)
