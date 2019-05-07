from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../"))

import os
import json
from common.logutils import get_logger


SMARTSCALER_NAME = "CYCLIC"

CONFIGURATION = {}

logger = get_logger(__name__)


def load_configuration():
    CONFIGURATION["Deployment"] = os.environ['SMARTSCALER_DEPLOYMENT']
    CONFIGURATION["Parameters"] = json.loads(os.environ['SMARTSCALER_PARAMETERS'])
    CONFIGURATION["MinReplicas"] = int(os.environ['SMARTSCALER_MIN_REPLICAS'])
    CONFIGURATION["MaxReplicas"] = int(os.environ['SMARTSCALER_MAX_REPLICAS'])


def print_configuration():
    logger.info("Smart Scaler {} running with configuration: {}".format(SMARTSCALER_NAME, CONFIGURATION))


if __name__ == "__main__":
    load_configuration()
    print_configuration()