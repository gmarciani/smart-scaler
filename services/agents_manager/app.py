import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.agents_manager.control.smart_scaling_loop import smart_scaling_loop_job as smart_scaling_loop_job
from services.agents_manager.config import Debug as AppConfig
from services.agents_manager.api.status import Status


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Scheduler
app.add_scheduled_job(smart_scaling_loop_job(app.app_context()))

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    app.start(port=app.config["AGENTS_MANAGER_PORT"])