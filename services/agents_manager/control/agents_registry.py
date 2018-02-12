from flask import g
from services.agents_manager.model.agents_registry import SimpleAgentsRegistry as AgentsRegistry


AGENTS_REGISTRY = AgentsRegistry()


def get_local_registry():
    """
    Retrieve the registry.
    :return: (dict) the registry.
    """
    return AGENTS_REGISTRY