import requests
import json
from services.common.control import connections as conn_ctrl
from services.common.exceptions.kubernetes_exception import KubernetesException


def get_state(kubernetes_conn):
    """
    Get the status of Kubernetes cluster.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :return: (dict) the Kubernetes status.
    """
    url = conn_ctrl.format_url("status", kubernetes_conn)

    try:
        response = requests.get(url)
        response_json = response.json()
    except requests.ConnectionError:
        return {"kube_state": "KUBERNETES UNREACHABLE"}
    return response_json


def get_all_smart_scalers(kubernetes_conn):
    """
    Get the list of Smart Scalers.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :return: (list) the list of Smart Scalers.
    """
    url = conn_ctrl.format_url("smart_scalers", kubernetes_conn)

    try:
        response = requests.get(url)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "get_all_smart_scalers: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    return response_json["smart_scalers"]


def get_all_kube_pods(kubernetes_conn):
    """
    Get the list of Pods.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :return: (list) the list of Pods.
    """
    url = conn_ctrl.format_url("pods", kubernetes_conn)

    try:
        response = requests.get(url)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "get_all_kube_pods: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    return response_json["pods"]


def get_pod_status(kubernetes_conn, pod_name):
    """
    Get the status of the specified Pod.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param pod_name: (string) the Pod name.
    :return: (dict) the status of the specified Pod.
    """
    url = conn_ctrl.format_url("pods/status", kubernetes_conn)

    data = {
        "name": pod_name
    }

    try:
        response = requests.get(url, params=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "get_pod_status: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    return response_json["status"]


def set_pod_replicas(kubernetes_conn, pod_name, replicas):
    """
    Set the replication degree for the specified Pod.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param pod_name: (string) the Pod name.
    :param replicas: (int) the Pod replication degree.
    :return: (tuple(integer,integer)) the old and new replication degree.
    """
    url = conn_ctrl.format_url("pods/scale", kubernetes_conn)

    data = {"name": pod_name, "replicas": replicas}

    try:
        response = requests.post(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "set_pod_replicas: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    return response_json["replicas_old"], response_json["pod_scaled"]["replicas"]