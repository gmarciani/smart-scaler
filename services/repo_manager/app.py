from flask import Flask
from api_repo_manager.status import status
from api_repo_manager.repo import repo
import logging


# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging._nameToLevel[app.config["LOG_LEVEL"]])

# Routes
app.register_blueprint(status)
app.register_blueprint(repo)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REPO_MANAGER_PORT"], threaded=True)
