"""
The REST API for the service status management.
"""


from flask_restful import Resource
from services.common.control import status as status_ctrl


class Status(Resource):
    """
    The Flask resource realizing the REST API for the service status management.
    """

    def get(self):
        """
        Get the status of the service.

        Returns
        -------
        res : dict
            The response.
        """
        return status_ctrl.compose_status_fake()