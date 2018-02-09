from flask_restful import Api
from services.api_gateway.api.status import Status
from datetime import datetime
from flask import jsonify


def configure(app):
    """
    Configure the app REST interface.
    :param app: the application.
    :return: None
    """
    api = Api(app)

    @api.representation("application/json")
    def output_json(data, code, headers=None):
        data["timestamp"] = datetime.now()
        return jsonify(data)

    api.add_resource(Status, "/status")