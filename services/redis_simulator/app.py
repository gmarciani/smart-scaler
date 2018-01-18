from flask import Flask
from api_redis_simulator.status import status
from api_redis_simulator.database import database
import logging


# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging._nameToLevel[app.config["LOG_LEVEL"]])

# Routes
app.register_blueprint(status)
app.register_blueprint(database)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REDIS_PORT"], threaded=True)
