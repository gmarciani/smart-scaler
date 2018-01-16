from flask import Flask
from api.status import status
from control.scheduler import MainScheduler
from control.jobs import shutdown_hook
import atexit

# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Routes
app.register_blueprint(status)

# Scheduled Jobs
AGENTS = {}
scheduler = MainScheduler(app.config["KUBERNETES_HOST"], app.config["KUBERNETES_PORT"], app.config["KUBERNETES_PULL"], AGENTS)
scheduler.start()

# Shutdown Hooks
atexit.register(shutdown_hook, "My Shutdown Param")
atexit.register(lambda: scheduler.shutdown_hook())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"], threaded=True)
