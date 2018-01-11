from datetime import datetime
import model.kube_state as kube_state


def increment_counter(value):
    t = datetime.now()
    kube_state.counter += value
    print("Cron Jobs launched at {}: increment {} | variable {}", datetime.now(), value, kube_state.counter)


def shutdown_hook(param):
    print("Shutdown Hook at {}: {}", datetime.now(), param)