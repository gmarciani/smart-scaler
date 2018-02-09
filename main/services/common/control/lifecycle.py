import atexit


def add_teardown_hook(app, func, *args, **kwargs):
    """
    Register a teardown hook.
    :param app: the application.
    :param func: the function.
    :param args: optional arguments to pass to func.
    :param kwargs: optional keyword arguments to pass to func.
    :return: None
    """
    app.teardown_appcontext(func)


def add_shutdown_hook(func, *args, **kwargs):
    """
    Register a shutdown hook.
    :param func: the function.
    :param args: optional arguments to pass to func.
    :param kwargs: optional keyword arguments to pass to func
    :return: None
    """
    if args is None and kwargs is None:
        atexit.register(func)
    else:
        atexit.register(func)