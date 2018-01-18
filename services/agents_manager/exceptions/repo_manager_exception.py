class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    pass


class RepositoryManagerException(Error):
    """
    Exception raised for errors in RepoManager.
    """

    def __init__(self, code, message):
        """
        Create a new exceptions.
        :param code: the error code.
        :param message: the error message.
        """
        self.code = code
        self.message = message