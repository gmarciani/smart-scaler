"""
The Flask application that realizes the service 'Agent'.
"""

from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.agents_manager.control.scheduler_jobs import registry_sync_job as smart_scaling_loop_job
from services.agents_manager.config import Debug as AppConfig
from services.agents_manager.api.status import Status


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Scheduler
app.add_scheduled_job(sync_loop_job(app.app_context()))

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    app.start(port=app.config["AGENTS_MANAGER_PORT"])