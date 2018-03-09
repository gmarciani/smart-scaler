"""
The Agents Manager Registry.
"""


class SimpleAgentsManagerRegistry:
    """
    A simple implementation of an Agents Manager Registry.
    """

    def __init__(self):
        """
        Create a new registry.
        """
        self._registry = {}  # name: (resource, aid), w.r.t. smart scalers

    def names(self):
        """
        Get all names.

        :return: the list of names.
        """
        return self._registry.keys()

    def resources(self):
        """
        Get all resources

        :return: the list of resources.
        """
        return self._registry.values()

    def __iter__(self):
        """
        The iteration method.

        :return: the iterator.
        """
        return self._registry.__iter__()

    def __str__(self):
        """
        Return the string representation.

        :return: the string representation.
        """
        return "AgentsManagerRegistry({})".format(self._registry)

    def __repr__(self):
        """
        Return the representation.

        :return: the representation.
        """
        return self._registry.__str__()