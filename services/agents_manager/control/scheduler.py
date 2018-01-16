from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from control.jobs import main_loop


class MainScheduler(BackgroundScheduler):

    def __init__(self, kube_host, kube_port, interval, agents):
        """
        Create a new *MainScheduler*.
        :param kube_host: (string) the Kubernetes host.
        :param kube_port: (int) the Kubernetes port.
        :param interval: (int) the pulling interval (seconds) to interact with Kubernetes.
        :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
        """
        BackgroundScheduler.__init__(self)

        self.kube_host = kube_host
        self.kube_port = kube_port
        self.agents = agents
        self.interval = interval

    def start(self):
        """
        Start the scheduler.
        :return: (void)
        """
        BackgroundScheduler.start(self)

        self.add_job(id="update_agents", func=main_loop,
                      kwargs={"kube_host": self.kube_host, "kube_port": self.kube_port, "agents": self.agents},
                      trigger=IntervalTrigger(seconds=self.interval), max_instances=1, coalesce=True)

    def shutdown_hook(self):
        """
        Perform all shutdown actions.
        :return: (void)
        """
        BackgroundScheduler.shutdown(self)