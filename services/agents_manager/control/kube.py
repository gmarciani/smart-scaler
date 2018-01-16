import requests
import json


def get_all_kube_smart_scalers(kube_host, kube_port):
    """
    Get the list of Smart Scalers.
    :param kube_host: (string) the Kubernetes host.
    :param kube_port: (int) the Kubernetes port.
    :return: (list) the list of Smart Scalers.; None, if error.
    """
    url = "http://{}:{}/smart_scalers".format(kube_host, kube_port)

    try:
        response = requests.get(url, timeout=5)
        return response.json()["smart_scalers"] if response is not None else None
    except requests.ConnectionError or requests.ReadTimeout or json.decoder.JSONDecodeError as exc:
        print("Error: ", str(exc))
        return None


def get_all_kube_pods(kube_host, kube_port):
    """
    Get the list of Pods.
    :param kube_host: (string) the Kubernetes host.
    :param kube_port: (int) the Kubernetes port.
    :return: (list) the list of Pods; None, if error.
    """
    url = "http://{}:{}/pods".format(kube_host, kube_port)

    try:
        response = requests.get(url, timeout=5)
        return response.json()["pods"] if response is not None else None
    except requests.ConnectionError or requests.ReadTimeout as exc:
        print("Error: ", str(exc))
        return None


def get_pod_status(kube_host, kube_port, pod_name):
    """
    Get the status of the specified Pod.
    :param kube_host: (string) the Kubernetes host.
    :param kube_port: (int) the Kubernetes port.
    :param pod_name: (string) the Pod name.
    :return: (dict) the status of the specified Pod; None, if error.
    """
    url = "http://{}:{}/pods/status".format(kube_host, kube_port)

    try:
        response = requests.get(url, params={"name": pod_name}, timeout=5)
        return response.json() if response is not None else None
    except requests.ConnectionError or requests.ReadTimeout as exc:
        print("Error: ", str(exc))
        return None


def set_pod_replicas(kube_host, kube_port, pod_name, replicas):
    """
    Set the replication degree for the specified Pod.
    :param kube_host: (string) the Kubernetes host.
    :param kube_port: (int) the Kubernetes port.
    :param pod_name: (string) the Pod name.
    :param replicas: (int) the Pod replication degree.
    :return: (bool) True if success; False, otherwise.
    """
    url = "http://{}:{}/pods/scale".format(kube_host, kube_port)

    data = {"name": pod_name, "replicas": replicas}
    try:
        response = requests.post(url, json=data, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError or requests.ReadTimeout as exc:
        print("Error: ", str(exc))
        return False
