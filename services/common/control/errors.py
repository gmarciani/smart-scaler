from werkzeug.exceptions import default_exceptions
from services.common.control import exception_handler as error_ctrl


def configure(app):
    """
    Configure the exception handling system.
    :param app: the application
    :return: None
    """
    for exc in default_exceptions:
        app.register_error_handler(exc, error_ctrl.handle_exception)
    app.register_error_handler(Exception, error_ctrl.handle_exception)