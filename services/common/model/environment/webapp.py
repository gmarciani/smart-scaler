from collections import OrderedDict
from flask import request, current_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED
from flask import Flask
from flask_restful import Api
from werkzeug.exceptions import default_exceptions
from services.common.control import exception_handler as error_ctrl
from services.common.util.jsonutil import output_json as output_json, SimpleJSONEncoder
import atexit
import logging

from services.common.util.logutils import ConsoleHandler

FORMATTER = logging.Formatter("%(asctime)s %(levelname)-6s [%(name)-50s:%(lineno)s] %(message)s")

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
        self.json_encoder = SimpleJSONEncoder
        self.api.representations = OrderedDict(REPRESENTATIONS)

        # Error Handling
        for exc in default_exceptions:
            self.register_error_handler(exc, error_ctrl.handle_exception)
        self.register_error_handler(Exception, error_ctrl.handle_exception)

        # Logging
        level = logging._nameToLevel[self.config["LOG_LEVEL"]]

        logging.basicConfig(level=level, handlers=[ConsoleHandler(level, FORMATTER)])
        logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)
        logging.getLogger("apscheduler.executors.default").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("redis_lock").setLevel(logging.ERROR)
        self.logger.setLevel(level)
        for hdlr in self.logger.handlers:
            hdlr.setFormatter(FORMATTER)

        # Scheduler
        self.scheduler = None

    def start(self, host="0.0.0.0", port=None):
        """
        Start the application.
        :param host: the server address.
        :param port: the server port number
        :return: None
        """
        if self.scheduler is not None:
            self.scheduler.start()
        Flask.run(self, host, port, threaded=True, use_reloader=False)

    def shtudown(self):
        """
        Shutdown the application.
        :return: None
        """
        fn_shutdown = request.environ.get("werkzeug.server.shutdown")
        if fn_shutdown is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        fn_shutdown()

    def add_rest_api(self, res, url):
        """
        Register a REST interface.
        :param res: the resource.
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

    def add_scheduled_job(self, job):
        """
        Add a scheduler.
        :param job: a scheduler job
        :return: None
        """
        if self.scheduler is None:
            self.scheduler = BackgroundScheduler()
            self.add_shutdown_hook(self._shutdown_scheduler)

        self.scheduler.add_job(id=job.name, func=job.func, kwargs=job.kwargs,
                               trigger=job.trigger, max_instances=1, coalesce=True)

    def _start_scheduler(self):
        """
        Start the app scheduler.
        :return: None
        """
        self.scheduler.start()

    def _shutdown_scheduler(self):
        """
        Shut down the app scheduler.
        :return: None
        """
        if self.scheduler is not None and self.scheduler.state is not STATE_STOPPED:
            self.scheduler.shutdown()
