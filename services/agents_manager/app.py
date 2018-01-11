from flask import Flask
from api.status import status
from api.kube import kube
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from control.jobs import increment_counter, shutdown_hook
import atexit

# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Routes
app.register_blueprint(status)
app.register_blueprint(kube)

# Cron Jobs
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=increment_counter,
    kwargs={"value": 1},
    trigger=IntervalTrigger(seconds=5),
    replace_existing=True)

# Shutdown Hooks
atexit.register(shutdown_hook, "My Shutdown Param")
atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"])
