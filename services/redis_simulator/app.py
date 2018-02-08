from services.common.environment.webapp import WebApp as App
from services.common.control import shutdown as shutdown_ctrl
from services.redis_simulator.config import Debug as AppConfig
from services.redis_simulator.api.status import Status
from services.redis_simulator.api.database import Database
from services.redis_simulator.control import database as database_ctrl


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")
app.add_rest_api(Database, "/database")

# Teardown
app.add_teardown_hook(database_ctrl.teardown_database)

# Shutdown
app.add_shutdown_hook(shutdown_ctrl.goodbye)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REPOSITORY_PORT"], threaded=True)
