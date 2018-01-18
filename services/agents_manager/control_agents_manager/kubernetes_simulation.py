import requests
import json
from exceptions.kubernetes_exception import KubernetesException


def get_all_kube_smart_scalers(kubernetes_conn):
    """
    Get the list of Smart Scalers.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :return: (list) the list of Smart Scalers.
    """
    host = kubernetes_conn[0]
    port = kubernetes_conn[1]

    url = "http://{}:{}/smart_scalers".format(host, port)

    response = requests.get(url)

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response.json()["error"])

    response_json = response.json()

    return response_json["smart_scalers"]


def get_all_kube_pods(kubernetes_conn):
    """
    Get the list of Pods.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :return: (list) the list of Pods.
    """
    host = kubernetes_conn[0]
    port = kubernetes_conn[1]

    url = "http://{}:{}/pods".format(host, port)

    response = requests.get(url)

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response.json()["error"])

    response_json = response.json()

    return response_json["pods"]


def get_pod_status(kubernetes_conn, pod_name):
    """
    Get the status of the specified Pod.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param pod_name: (string) the Pod name.
    :return: (dict) the status of the specified Pod.
    """
    host = kubernetes_conn[0]
    port = kubernetes_conn[1]

    url = "http://{}:{}/pods/status".format(host, port)

    data = {
        "name": pod_name
    }

    response = requests.get(url, params=data)

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response.json()["error"])

    response_json = response.json()

    return response_json["status"]


def set_pod_replicas(kubernetes_conn, pod_name, replicas):
    """
    Set the replication degree for the specified Pod.
    :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
    :param pod_name: (string) the Pod name.
    :param replicas: (int) the Pod replication degree.
    :return: (tuple(integer,integer)) the old and new replication degree.
    """
    host = kubernetes_conn[0]
    port = kubernetes_conn[1]

    url = "http://{}:{}/pods/scale".format(host, port)

    data = {"name": pod_name, "replicas": replicas}

    response = requests.post(url, json=data)

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response.json()["error"])

    response_json = response.json()

    return response_json["replicas_old"], response_json["pod_scaled"]["replicas"]


