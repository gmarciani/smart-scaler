from collections import OrderedDict

from flask import Flask
from flask_restful import Api
from services.common.environment.responses import output_json
from werkzeug.exceptions import default_exceptions
from services.common.control import exception_handler as error_ctrl
import atexit
import logging


FORMAT = "[%(name)s:%(lineno)s - %(funcName)30s] %(message)s"

REPRESENTATIONS = [("application/json", output_json)]


class WebApp(Flask):
    """
    A web application.
    """

    def __init__(self, name, config):
        """
        Create a new web application.
        :param name: the application name.
        :param config: the configuration.
        """
        Flask.__init__(self, name)
        self.config.from_object(config)
        self.api = Api(self)

        # JSON Response
        self.api.representations = OrderedDict(REPRESENTATIONS)

        # Error Handling
        if not self.config["DEBUG"]:
            for exc in default_exceptions:
                self.register_error_handler(exc, error_ctrl.handle_exception)
            self.register_error_handler(Exception, error_ctrl.handle_exception)

        # Logging
        logging.basicConfig(level=logging._nameToLevel[self.config["LOG_LEVEL"]], format=FORMAT)
        logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
        logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.FATAL)

    def add_rest_api(self, res, url):
        """
        Register a REST interface.
        :param resource: the resource.
        :param url: the url.
        :return: None
        """
        self.api.add_resource(res, url)

    def add_teardown_hook(self, func, *args, **kwargs):
        """
        Register a teardown hook.
        :param func: the function.
        :param args: optional arguments to pass to func.
        :param kwargs: optional keyword arguments to pass to func
        :return: None
        """
        self.teardown_appcontext(func)

    def add_shutdown_hook(self, func, *args, **kwargs):
        """
        Register a shutdown hook.
        :param func: the function.
        :param args: optional arguments to pass to func.
        :param kwargs: optional keyword arguments to pass to func
        :return: None
        """
        if args is None and kwargs is None:
            atexit.register(func)
        else:
            atexit.register(func)