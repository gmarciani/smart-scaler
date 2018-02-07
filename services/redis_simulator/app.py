from flask import Flask
from services.common.control import logs as log_config
from services.common.control import errors as err_config
from services.common.control import lifecycle as lifecycle_config
from services.common.control import shutdown as shutdown_ctrl

from services.redis_simulator.config import Debug as AppConfig
from services.redis_simulator.rest import api as api_config
from services.redis_simulator.control import database as database_ctrl


# Initialization
app = Flask(__name__)
app.config.from_object(AppConfig)

# REST API
api_config.configure(app)

# Configure logging
log_config.configure(app)

# Errors
err_config.configure(app)

# Teardown
lifecycle_config.add_teardown_hook(app, database_ctrl.teardown_database)

# Shutdown
lifecycle_config.add_shutdown_hook(shutdown_ctrl.goodbye)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REPOSITORY_PORT"], threaded=True)
