import logging


FORMAT = "[%(name)s:%(lineno)s - %(funcName)30s] %(message)s"


def configure(app):
    """
    Configure the logging system.
    :param app: the app instance.
    :param log_level: (string) the log level name.
    :return: None
    """
    log_level = app.config["LOG_LEVEL"]
    logging.basicConfig(level=logging._nameToLevel[log_level], format=FORMAT)
    logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.FATAL)


