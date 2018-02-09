from flask_restful import Resource
from flask import request
from services.common.model.exception import NotFound, BadRequest
from services.redis_simulator.control import database as database_ctrl


class Database(Resource):
    """
    Database.
    """
    def get(self):
        """
        Get the value of the key.
        :return: the response.
        """
        data = request.args

        if "key" not in data:  # get all values
            return dict(values=database_ctrl.get_database())

        else:  # get the value for the given key
            key = data["key"]

            try:
                value = database_ctrl.get_database()[key]
            except KeyError:
                raise NotFound("Cannot find key {}".format(key))

            return dict(key=key, value=value)

    def put(self):
        """
        Set the value of the key, that must be unique.
        :return: the response.
        """
        data = request.get_json()

        try:
            key = data["key"]
            value = data["value"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'key', 'value'")

        if key in database_ctrl.get_database():
            raise BadRequest("Cannot create key {} because it already exists".format(key))

        database_ctrl.get_database()[key] = value

        return dict(key=key, value=value)

    def post(self):
        """
        Set the value of the key.
        :return: the response.
        """
        data = request.get_json()

        try:
            key = data["key"]
            value_new = data["value"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'key', 'value'")

        try:
            value_old = database_ctrl.get_database()[key]
        except KeyError:
            value_old = None

        database_ctrl.get_database()[key] = value_new

        return dict(key=key, value_new=value_new, value_old=value_old)

    def patch(self):
        """
        Update the value of the existent key.
        :return: (json) the response.
        """
        data = request.get_json()

        try:
            key = data["key"]
            value_new = data["value"]
        except KeyError:
            raise BadRequest("Cannot find field(s) 'key', 'value'")

        try:
            value_old = database_ctrl.get_database()[key]
        except KeyError:
            raise NotFound("Cannot find key {}".format(key))

        database_ctrl.get_database()[key] = value_new

        return dict(key=key, value_new=value_new, value_old=value_old)

    def delete(self):
        """
        Delete the key.
        :return: (json) the response.
        """
        data = request.get_json()

        try:
            key = data["key"]
        except KeyError:
            raise BadRequest("Cannot find field 'key'")

        try:
            value = database_ctrl.get_database()[key]
        except KeyError:
            raise NotFound("Cannot find key {}".format(key))

        del database_ctrl.get_database()[key]

        return dict(key=key, value=value)