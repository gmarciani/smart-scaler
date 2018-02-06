class SimpleConnection:

    def __init__(self, host, port):
        """
        Create a new connection.
        :param host: (string) the hostname.
        :param port:  (int) the port number.
        """
        self.host = host
        self.port = port

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "Connection({}:{})".format(self.host, self.port)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()