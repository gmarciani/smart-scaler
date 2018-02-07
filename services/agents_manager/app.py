from flask import Flask
from common.control import logs as log_configurator
from services.agents_manager.api.status import status as api_status
from services.agents_manager.control import scheduler as scheduler_ctrl
from services.common.control import shutdown as shutdown_ctrl
import logging


# Initialization
app = Flask(__name__)
app.config.from_object("config.Debug")

# Configure logging
log_configurator.configure(logging, app.config["LOG_LEVEL"])

# Routes
app.register_blueprint(api_status)

# Scheduled Jobs
scheduler_ctrl.get_scheduler().start()


# Teardown Hooks
@app.teardown_appcontext
def teardown(exception):
    scheduler_ctrl.teardown_scheduler()
    shutdown_ctrl.goodbye()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"], threaded=True)