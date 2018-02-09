from services.common.environment.webapp import WebApp as App
from services.common.control import shutdown as shutdown_ctrl
from services.agents_manager.config import Debug as AppConfig
from services.agents_manager.api.status import Status


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Teardown
#app.add_teardown_hook(database_ctrl.teardown_database)

# Shutdown
app.add_shutdown_hook(shutdown_ctrl.goodbye)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"], threaded=True)