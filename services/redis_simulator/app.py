"""
The Flask application that realizes the service 'Redis Simulator'.
"""


from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.redis_simulator.config import Debug as AppConfig
from services.redis_simulator.api.status import Status
from services.redis_simulator.api.database import Database
from services.redis_simulator.control import database as database_ctrl
from sys import argv


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")
app.add_rest_api(Database, "/database")

# Teardown
app.add_teardown_hook(database_ctrl.teardown_database)

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    if len(argv) > 1:
        app.config["REPOSITORY_PORT"] = int(argv[1])
    app.start(port=app.config["REPOSITORY_PORT"])
