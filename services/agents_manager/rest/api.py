from flask_restful import Api
from services.redis_simulator.api.status import Status
from services.redis_simulator.api.database import Database
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
    api.add_resource(Database, "/database")