from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from control_agents_manager.jobs import main_loop


class MainScheduler(BackgroundScheduler):

    def __init__(self, kubernetes_conn, repo_manager_conn, agents, kubernetes_pull):
        """
        Create a new *MainScheduler*.
        :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
        :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
        :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
        :param kubernetes_pull: (int) the pulling interval (seconds) to interact with Kubernetes.
        """
        BackgroundScheduler.__init__(self)

        self.kubernetes_conn = kubernetes_conn
        self.repo_manager_conn = repo_manager_conn
        self.agents = agents
        self.kubernetes_pull = kubernetes_pull

    def start(self):
        """
        Start the scheduler.
        :return: (void)
        """
        BackgroundScheduler.start(self)

        self.add_job(id="update_agents", func=main_loop,
                      kwargs={"kubernetes_conn": self.kubernetes_conn, "repo_manager_conn": self.repo_manager_conn, "agents": self.agents},
                      trigger=IntervalTrigger(seconds=self.kubernetes_pull), max_instances=1, coalesce=True)

    def shutdown_hook(self):
        """
        Perform all shutdown actions.
        :return: (void)
        """
        BackgroundScheduler.shutdown(self)