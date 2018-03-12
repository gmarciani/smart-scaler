"""
The Flask application that realizes the service 'Kubernetes Simulator'.
"""


from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../../"))

from services.common.model.environment.webapp import WebApp as App
from services.kubernetes_simulator.config import Debug as AppConfig
from services.kubernetes_simulator.api.status import Status
from services.kubernetes_simulator.api.registry_pods import Pods
from services.kubernetes_simulator.api.registry_smart_scalers import SmartScalers
from services.kubernetes_simulator.api.heapster import PodMetrics
from services.kubernetes_simulator.control import heapster as heapster_ctrl
from services.kubernetes_simulator.control import registry as registry_ctrl
from sys import argv


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")
app.add_rest_api(Pods, "/registry/pods")
app.add_rest_api(SmartScalers, "/registry/smart_scalers")
app.add_rest_api(PodMetrics, "/heapster/pods")

# Teardown
app.add_teardown_hook(registry_ctrl.teardown_registry)
app.add_teardown_hook(heapster_ctrl.teardown_heapster)

# Shutdown
app.add_shutdown_hook(lambda: print("Goodbye!"))


if __name__ == "__main__":
    if len(argv) > 1:
        app.config["KUBERNETES_PORT"] = int(argv[1])
    app.start(port=app.config["KUBERNETES_PORT"])
