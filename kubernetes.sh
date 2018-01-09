#!/bin/bash

HOME_DIR = "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

API_GATEWAY_CONTAINER = "api_gateway"
API_GATEWAY_IMAGE = "smart_scaler_api_gateway"
API_GATEWAY_IMAGE_VERSION = "1.0.0"
API_GATEWAY_DOCKER_PATH = "${HOME_DIR}/services/api_gateway"
API_GATEWAY_PORT = 18001

AGENTS_MANAGER_CONTAINER = "agents_manager"
AGENTS_MANAGER_IMAGE = "smart_scaler_agents_manager"
AGENTS_MANAGER_IMAGE_VERSION = "1.0.0"
AGENTS_MANAGER_DOCKER_PATH = "${HOME_DIR}/services/agents_manager"
AGENTS_MANAGER_PORT = 18002

REPO_MANAGER_CONTAINER = "repo_manager"
REPO_MANAGER_IMAGE = "smart_scaler_repo_manager"
REPO_MANAGER_IMAGE_VERSION = "1.0.0"
REPO_MANAGER_DOCKER_PATH = "${HOME_DIR}/services/repo_manager"
REPO_MANAGER_PORT = 18003

REDIS_CONTAINER = "redis"
REDIS_IMAGE = "redis"
REDIS_IMAGE_VERSION = "latest"
REDIS_PORT = 6379