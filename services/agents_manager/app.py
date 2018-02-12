from services.common.model.environment.webapp import WebApp as App
from services.agents_manager.control.jobs.smart_scaling_loop import smart_scaling_loop_job as smart_scaling_loop_job
from services.common.control import shutdown as shutdown_ctrl
from services.agents_manager.config import Debug as AppConfig
from services.agents_manager.api.status import Status


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Scheduler
app.add_scheduled_job(smart_scaling_loop_job(app.app_context()))

# Shutdown
app.add_shutdown_hook(shutdown_ctrl.goodbye)


if __name__ == "__main__":
    app.start(port=app.config["AGENTS_MANAGER_PORT"])