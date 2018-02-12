from services.common.model.exceptions.service_exception import ServiceException


class KubernetesException(ServiceException):
    """
    Exception raised for errors in Kubernetes.
    """

    def __init__(self, code, message):
        """
        Create a new exceptions.
        :param code: the error code.
        :param message: the error message.
        """
        self.code = code
        self.message = message