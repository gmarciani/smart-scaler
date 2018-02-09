import logging



class SchedulerFilterNoLog(logging.Filter):
    """
    Filter to exclude all APScheduler messages.
    """
    def filter(self, record):
        return False


class SchedulerFilter(logging.Filter):
    """
    Filter to exclude some APScheduler messages.
    """
    def filter(self, record):
        return not record.msg.startswith("Running job")
