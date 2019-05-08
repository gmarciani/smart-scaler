from sys import path as pythonpath
from os.path import join, dirname, realpath
pythonpath.append(join(dirname(realpath(__file__)), "../"))

import os
import json
from kubernetes import client, config
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


def make_step():
    config.load_incluster_config()

    api = client.ExtensionsV1beta1Api()
    logger.info("Getting Deployment: {}".format(CONFIGURATION['Deployment']))
    try:
        deployment = api.read_namespaced_deployment(CONFIGURATION['Deployment'], 'DEFAULT')
        print("Deployment Details: {}".format(deployment))
    except client.rest.ApiException as e:
        logger.error("Cannot find Deployment {}".format(CONFIGURATION['Deployment']))


if __name__ == "__main__":
    load_configuration()
    print_configuration()
    make_step()