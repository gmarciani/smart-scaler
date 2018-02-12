from apscheduler.triggers.interval import IntervalTrigger
from services.common.model.scheduler import SimpleJob as SchedulerJob
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def print_hello_job():
    """
    Create the scheduler job 'print_hello'.
    :return: the scheduler job.
    """
    return SchedulerJob(name="print_hello", func=print_hello, trigger=IntervalTrigger(seconds=10))


def print_hello():
    """
    Print hello message with datetime.
    :return: None
    """
    print("Hello {}".format(datetime.now()))