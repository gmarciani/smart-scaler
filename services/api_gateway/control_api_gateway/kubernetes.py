import requests


def get_state(kube_host, kube_port):
    """
    Get the status of Kubernetes cluster.
    :return: (dict) the Kubernetes status.
    """
    url_kube_state_service = "http://{}:{}/status".format(kube_host, kube_port)

    try:
        return requests.get(url_kube_state_service, timeout=5).json()
    except requests.ConnectionError:
        return {"kube_state": "KUBERNETES UNREACHABLE"}