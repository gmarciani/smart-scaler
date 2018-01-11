from flask import Blueprint, current_app
from flask import jsonify
from datetime import datetime
# from kubernetes import client as k8s_client
# from kubernetes import config as k8s_config
import model.kube_state as kube_state


kube = Blueprint("kube", __name__)

#k8s_config.load_kube_config()


#@kube.route("/kube/pods", methods={"GET"})
#def get_pods():
#    v1 = k8s_client.CoreV1Api()
#
#    pods = v1.list_pod_for_all_namespaces(watch=False)
#    print(pods)
#
#    reponse = {
#        "ts": datetime.now(),
#        "pods": pods
#    }
#
#    return jsonify(reponse)


@kube.route("/kube/state", methods=["GET"])
def get_k8s_state():
    response = {
        "ts": datetime.now(),
        "state": kube_state.counter
    }

    return jsonify(response)







