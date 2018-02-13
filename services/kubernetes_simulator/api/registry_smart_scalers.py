from flask_restful import Resource
from flask import request

from services.common.model.resources.smart_scaler_resource import SmartScalerResource
from services.common.model.exceptions.rest_exceptions import NotFound, BadRequest
from services.kubernetes_simulator.control import registry as registry_ctrl
from copy import deepcopy


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
            return dict(smart_scalers=list(registry_ctrl.get_registry().get_smart_scalers().values()))

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
            min_replicas = data["min_replicas"]
            max_replicas = data["max_replicas"]
            ai_technique = data["ai_technique"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'name', 'pod_name', 'min_replicas', 'max_replicas', 'ai_technique'")

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

        try:
            ai_params = data["ai_params"]
        except KeyError:
            ai_params = {}

        smart_scaler_new = SmartScalerResource(smart_scaler_name, pod_name, min_replicas, max_replicas, ai_technique)
        smart_scaler_new.ai_params = ai_params
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