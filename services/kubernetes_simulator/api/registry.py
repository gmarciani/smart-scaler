from flask_restful import Resource
from flask import request

from services.common.model.smart_scaler import SmartScaler
from services.common.model.exception import NotFound, BadRequest
from services.common.model.pod import Pod as Pod
from services.kubernetes_simulator.control import registry as registry_ctrl
from copy import deepcopy


class Pods(Resource):
    """
    Pods in Kubernetes Registry.
    """

    def get(self):
        """
        Get all Pods or specific Pod.
        :return: the response.
        """
        data = request.args

        if "name" not in data:  # get all pods
            return dict(pods=[vars(pod) for pod in registry_ctrl.get_registry().get_pods().values()])

        else:  # get specific pod
            pod_name = data["name"]

            try:
                pod = registry_ctrl.get_registry().get_pods()[pod_name]
            except KeyError:
                raise NotFound("Cannot find pod {}".format(pod_name))

            return dict(pod=pod)

    def put(self):
        """
        Create a new Pod.
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

        pod_new = Pod(pod_name, pod_replicas)
        registry_ctrl.get_registry().get_pods()[pod_name] = pod_new

        return dict(pod=pod_new)

    def patch(self):
        """
        Update the value of the existent pod.
        :return: the response.
        """
        data = request.get_json()

        try:
            pod_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field 'name'")

        try:
            pod = deepcopy(registry_ctrl.get_registry().get_pods()[pod_name])
        except KeyError:
            raise NotFound("Cannot find pod {}".format(pod_name))

        pod_old = deepcopy(pod)

        for k, v in list(filter(lambda k, v: k is not "name", data.items())):
            setattr(pod, k, v)

        return dict(pod=pod, pod_old=pod_old)

    def delete(self):
        """
        Delete a Pod.
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


class SmartScalers(Resource):
    """
    Smart Scalers in Kubernetes Registry.
    """

    def get(self):
        """
        Get all Smart Scalers or specific Smart Scaler.
        :return: the response.
        """
        data = request.args

        if "name" not in data:  # get all smart scalers
            return dict(pods=[vars(pod) for pod in registry_ctrl.get_registry().get_smart_scalers().values()])

        else:  # get specific smart scaler
            smart_scaler_name = data["name"]

            try:
                smart_scaler = registry_ctrl.get_registry().get_smart_scalers()[smart_scaler_name]
            except KeyError:
                raise NotFound("Cannot find smart scaler {}".format(smart_scaler_name))

            return dict(smart_scaler=smart_scaler)

    def put(self):
        """
        Create a new Smart Scaler.
        :return:
        """
        data = request.get_json()

        try:
            smart_scaler_name = data["name"]
            pod_name = data["pod_name"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'name', 'pod_name'")

        smart_scaler_min_replicas = int(data["min_replicas"]) if "min_replicas" in data else 1
        smart_scaler_max_replicas = int(data["max_replicas"]) if "max_replicas" in data else float("inf")

        if smart_scaler_name in registry_ctrl.get_registry().get_smart_scalers():
            raise BadRequest("Cannot create smart scaler {} because it already exists".format(smart_scaler_name))

        if pod_name not in registry_ctrl.get_registry().get_pods():
            raise BadRequest("Cannot create smart scaler {} because pod {} does not exist".format(smart_scaler_name,
                                                                                              pod_name))

        if any(smart_scaler.pod_name == pod_name for smart_scaler in
               registry_ctrl.get_registry().get_smart_scalers().values()):
            raise BadRequest(
                "Cannot create smart scaler {} because pod {} has been already associated to another smart scaler".format(
                    smart_scaler_name, pod_name))

        smart_scaler_new = SmartScaler(smart_scaler_name, pod_name, smart_scaler_min_replicas,
                                       smart_scaler_max_replicas)
        registry_ctrl.get_registry().get_smart_scalers()[smart_scaler_name] = smart_scaler_new

        return dict(smart_scaler=smart_scaler_new)

    def delete(self):
        """
        Delete a Smart Scaler.
        :return:
        """
        data = request.get_json()

        try:
            smart_scaler_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field 'name'")

        try:
            smart_scaler_deleted = deepcopy(registry_ctrl.get_registry().get_smart_scalers()[smart_scaler_name])
            del registry_ctrl.get_registry().get_smart_scalers()[smart_scaler_name]
        except KeyError:
            raise NotFound("Cannot find smart scaler {}".format(smart_scaler_name))

        return dict(smart_scaler=smart_scaler_deleted)