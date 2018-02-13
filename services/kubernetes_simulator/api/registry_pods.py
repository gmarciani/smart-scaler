from flask_restful import Resource
from flask import request
from services.common.model.resources.pod_resource import PodResource
from services.common.model.exceptions.rest_exceptions import NotFound, BadRequest
from services.kubernetes_simulator.control import registry as registry_ctrl
from copy import deepcopy


class Pods(Resource):
    """
    Pods in Kubernetes Registry.
    """

    def get(self):
        """
        Get all Pods or specific pod.
        :return: the response.
        """
        data = request.args

        if "name" not in data:  # get all pods
            return dict(pods=list(registry_ctrl.get_registry().get_pods().values()))

        else:  # get specific pod
            pod_name = data["name"]

            try:
                pod = registry_ctrl.get_registry().get_pods()[pod_name]
            except KeyError:
                raise NotFound("Cannot find pod {}".format(pod_name))

            return dict(pod=pod)

    def put(self):
        """
        Create a new pod.
        :return: the response
        """
        data = request.get_json()

        try:
            pod_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'name'")

        pod_replicas = int(data["replicas"]) if "replicas" in data else 1

        if pod_name in registry_ctrl.get_registry().get_pods():
            raise BadRequest("Cannot create pod {} because it already exists".format(pod_name))

        pod_new = PodResource(pod_name, pod_replicas)
        registry_ctrl.get_registry().get_pods()[pod_name] = pod_new

        return dict(pod=pod_new)

    def patch(self):
        """
        Update the value of an existing pod.
        :return: the response.
        """
        data = request.get_json()

        try:
            pod_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field 'name'")

        try:
            pod = registry_ctrl.get_registry().get_pods()[pod_name]
        except KeyError:
            raise NotFound("Cannot find pod {}".format(pod_name))

        pod_old = deepcopy(pod)

        for k,v in data.items():
            if k == "name":
                continue
            setattr(pod, k, v)

        return dict(pod=pod, pod_old=pod_old)

    def delete(self):
        """
        Delete a pod.
        :return: the response.
        """
        data = request.get_json()

        try:
            pod_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field 'name'")

        try:
            pod_deleted = deepcopy(registry_ctrl.get_registry().get_pods()[pod_name])
            del registry_ctrl.get_registry().get_pods()[pod_name]
        except KeyError:
            raise NotFound("Cannot find pod {}".format(pod_name))

        smart_scaler_name_to_delete = next(
            (x.name for x in registry_ctrl.get_registry().get_smart_scalers().values() if x.pod_name == pod_name), None)

        smart_scaler_deleted = None
        if smart_scaler_name_to_delete is not None:
            smart_scaler_deleted = deepcopy(
                registry_ctrl.get_registry().get_smart_scalers()[smart_scaler_name_to_delete])
            del registry_ctrl.get_registry().get_smart_scalers()[smart_scaler_name_to_delete]

        return dict(pod=pod_deleted, smart_scalers=smart_scaler_deleted)