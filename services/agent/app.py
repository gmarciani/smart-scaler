"""
The Flask application that realizes the service 'Agent'.
"""


from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.agent.control.agent_loop import agent_loop_job as agent_loop_job
from services.agent.config import Debug as AppConfig
from services.agent.api.status import Status
from sys import argv


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")

# Scheduler
app.add_scheduled_job(agent_loop_job(app.app_context()))

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    if len(argv) > 1:
        app.config["AGENT_PORT"] = int(argv[1])
    app.start(port=app.config["AGENT_PORT"])