class SimpleJob:
    """
    A simple scheduler job.
    """

    def __init__(self, name, func, trigger, kwargs=None):
        """
        Create a new scheduler job.
        :param name: the job name.
        :param func: the function to execute.
        :param trigger: the function trigger.
        :param kwargs: the arguments for the function.
        """
        self.name = name
        self.func= func
        self.kwargs = kwargs
        self.trigger = trigger