from services.common.environment.webapp import WebApp as App
from services.common.control import shutdown as shutdown_ctrl
from services.kubernetes_simulator.config import Debug as AppConfig
from services.kubernetes_simulator.api.status import Status
from services.kubernetes_simulator.api.registry import Pods, SmartScalers
from services.kubernetes_simulator.api.heapster import PodMetrics
from services.kubernetes_simulator.control import heapster as heapster_ctrl
from services.kubernetes_simulator.control import registry as registry_ctrl


# Initialization
app = App(__name__, AppConfig)

# REST API
app.add_rest_api(Status, "/status")
app.add_rest_api(Pods, "/registry/pods")
app.add_rest_api(SmartScalers, "/registry/smart_scalers")
app.add_rest_api(PodMetrics, "/heapster/pods")


# Teardown
app.add_teardown_hook(registry_ctrl.teardown_registry())
app.add_teardown_hook(heapster_ctrl.teardown_heapster())

# Shutdown
app.add_shutdown_hook(shutdown_ctrl.goodbye)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["KUBERNETES_PORT"], threaded=True)
