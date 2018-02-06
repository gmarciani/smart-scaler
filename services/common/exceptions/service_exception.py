class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    pass


class ServiceException(Error):
    """
    Base class for services exceptions.
    """

    def __init__(self, code, message):
        """
        Create a new exceptions.
        :param code: the error code.
        :param message: the error message.
        """
        self.code = code
        self.message = message