FORMAT = "[%(name)s:%(lineno)s - %(funcName)30s] %(message)s"


def configure_logging(logging, log_level):
    """
    Configure the logging system.
    :param logging: the logging instance.
    :param log_level: (string) the log level name.
    :return: (void)
    """
    logging.basicConfig(level=logging._nameToLevel[log_level], format=FORMAT)
    logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.FATAL)