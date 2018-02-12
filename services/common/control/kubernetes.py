import requests
import json

from services.common.model.exceptions.kubernetes_exception import KubernetesException
from services.common.model.resources.smart_scaler import SmartScalerResource
from services.common.model.resources.pod import PodResource
from services.common.control import connections as conn_ctrl
import logging


logger = logging.getLogger(__name__)


def get_all_smart_scalers(kubernetes_conn):
    """
    Get the list of smart scalers.
    :param kubernetes_conn: (SimpleConnection) the connection to Kubernetes.
    :return: (list) the list of smart scalers.
    """
    url = conn_ctrl.format_url("registry/smart_scalers", kubernetes_conn)

    try:
        response = requests.get(url)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "get_all_smart_scalers: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    smart_scalers = []

    for s in response_json["smart_scalers"]:
        try:
            smart_scalers.append(SmartScalerResource.from_json(s))
        except Exception:
            logger.error("Cannot parse smart scaler {}".format(s))

    return smart_scalers


def get_all_pods(kubernetes_conn):
    """
    Get the list of Pods.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :return: (list) the list of Pods.
    """
    url = conn_ctrl.format_url("registry/pods", kubernetes_conn)

    try:
        response = requests.get(url)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "get_all_kube_pods: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    pods = []

    for s in response_json["pods"]:
        try:
            pods.append(PodResource.from_json(s))
        except Exception:
            logger.error("Cannot parse pod {}".format(s))

    return pods


def get_pod(kubernetes_conn, pod_name):
    """
    Get the status of the specified Pod.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param pod_name: (string) the Pod name.
    :return: (Pod) the pod.
    """
    url = conn_ctrl.format_url("registry/pods", kubernetes_conn)

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

    s = response_json["pod"]
    try:
        pod = PodResource.from_json(s)
    except Exception:
        logger.error("Cannot parse pod {}".format(s))

    return pod


def set_pod_replicas(kubernetes_conn, pod_name, replicas):
    """
    Set the replication degree for the specified Pod.
    :param kubernetes_conn: (SimpleConnection) the Kubernetes connection.
    :param pod_name: (string) the Pod name.
    :param replicas: (int) the Pod replication degree.
    :return: (tuple(integer,integer)) the old and new replication degree.
    """
    url = conn_ctrl.format_url("registry/pods", kubernetes_conn)

    data = {"name": pod_name, "replicas": replicas}

    try:
        response = requests.patch(url, json=data)
        response_json = response.json()
    except (requests.ConnectionError, json.JSONDecodeError) as exc:
        raise KubernetesException(500, "set_pod_replicas: " + str(exc))

    if response.status_code is not 200:
        raise KubernetesException(response.status_code, response_json["error"])

    return response_json["replicas_old"], response_json["pod_scaled"]["replicas"]