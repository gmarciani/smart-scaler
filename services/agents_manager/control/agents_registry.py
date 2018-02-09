from flask import g
from services.agents_manager.model.agents_registry import SimpleAgentsRegistry as AgentsRegistry


def get_registry():
    """
    Retrieve the registry.
    :return: (dict) the registry.
    """
    registry = getattr(g, "_registry", None)
    if registry is None:
        registry = g._registry = __init_registry()
    return registry


def teardown_registry():
    """
    Teardown the registry.
    :return: (void)
    """
    registry = getattr(g, "_registry", None)
    if registry is not None:
        setattr(g, "_registry", None)


def __init_registry():
    """
    Create a new registry instance.
    :return: the new registry instance.
    """
    return AgentsRegistry()