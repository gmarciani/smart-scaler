"""
The REST API that realizes status management.
"""


from flask_restful import Resource
from services.common.control import status as status_ctrl


class Status(Resource):
    """
    Status of the service.
    """

    def get(self):
        """
        Get the status of the service.
        :return: the status of the service.
        """
        return status_ctrl.compose_status_fake()