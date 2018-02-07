from flask import current_app
from flask_restful import Resource
from services.common.control import status as status_ctrl


SERVICES = ["agents_manager", "repository", "kubernetes"]


class Status(Resource):
    """
    Status of the service.
    """

    def get(self):
        """
        Get the status of the service.
        :return: the status of the service.
        """
        return status_ctrl.compose_status_respose(status_ctrl.get_statuses(SERVICES, current_app.config))