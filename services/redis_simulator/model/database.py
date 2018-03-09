"""
The model that realizes a Redis Database.
"""


class SimpleRedisDatabase(dict):
    """
    A simple implementation of an Redis Database.
    """

    def __init__(self, *args, **kwargs):
        """
        Create a new Redis Database.

        Parameters
        ----------
        args : positional arguments
            Positional arguments.

        kwargs : dict
            Keyed arguments.

        Returns
        ----------
        : SimpleRedisDatabase
            A new instance of Redis Database.
        """
        super(SimpleRedisDatabase, self).__init__(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation.

        Returns
        ----------
        : str
            The string representation.
        """
        return "SimpleRedisDatabase({})".format(super(SimpleRedisDatabase, self).__str__())

    def __repr__(self):
        """
        Return the representation.

        Returns
        ----------
        : str
            The string representation.
        """
        return super(SimpleRedisDatabase, self).__repr__()