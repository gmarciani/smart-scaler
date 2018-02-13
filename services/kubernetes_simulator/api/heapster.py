from flask_restful import Resource
from flask import request
from services.common.model.exceptions.rest_exceptions import NotFound, BadRequest
from services.kubernetes_simulator.control import heapster as heapster_ctrl
from copy import deepcopy


class PodMetrics(Resource):
    """
    Metrics for Pods in Kubernetes.
    """

    def get(self):
        """
        Get metrics for a Pod.
        :return: the response.
        """
        data = request.args

        try:
            pod_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'name'")

        try:
            metrics = heapster_ctrl.get_heapster().get_pod_metrics()[pod_name]
        except KeyError:
            raise NotFound("Cannot find metrics for pod {}".format(pod_name))

        return dict(pod_name=pod_name, metrics=metrics)

    def patch(self):
        """
        Update metrics for a Pod.
        :return:
        """
        data = request.get_json()

        try:
            pod_name = data["name"]
        except KeyError:
            raise BadRequest("Cannot find field 'name'")

        try:
            metrics = deepcopy(heapster_ctrl.get_heapster().get_pod_metrics()[pod_name])
        except KeyError:
            raise NotFound("Cannot find pod {}".format(pod_name))

        metrics_old = deepcopy(metrics)

        for k, v in list(filter(lambda k, v: k is not "name", data.items())):
            setattr(metrics, k, v)

        return dict(pod_name=pod_name, metrics_new=metrics, metrics_old=metrics_old)