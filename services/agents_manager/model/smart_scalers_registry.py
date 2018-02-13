"""
Registry of smart scaling agents.
"""


class SimpleSmartScalersRegistry:
    """
    A simple registry of smart scaling agents.
    """

    def __init__(self):
        """
        Create a new registry of smart scaling agents.
        """
        self._registry = {}

    def values(self):
        return self._registry.values()

    def __iter__(self):
        return self._registry.__iter__()

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "AgentsRegistry({})".format(self._registry)

    def __repr__(self):
        """
        Return the representation.
        :return: (string) the representation.
        """
        return self._registry.__str__()