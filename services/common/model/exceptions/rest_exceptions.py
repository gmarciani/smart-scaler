class RESTException(Exception):
    """
    Simple REST exception.
    """

    def __init__(self, code, message):
        """
        Create a new REST exception.
        :param code: the HTTP error code.
        :param message: the error message.
        """
        self.code = code
        self.message = message


class NotFound(RESTException):

    def __init__(self, message):
        """
        Create a new Not Found exception.
        :param message: the HTTP error code.
        :param message: the error message.
        """
        RESTException.__init__(self, 404, message)


class BadRequest(RESTException):

    def __init__(self, message):
        """
        Create a new Bad Request exception.
        :param message: the error message.
        """
        RESTException.__init__(self, 400, message)
