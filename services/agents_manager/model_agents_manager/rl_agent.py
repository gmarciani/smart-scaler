from control_agents_manager import kubernetes_simulation as kubernetes_ctrl
from control_agents_manager import repo_manager as repo_manager_ctrl
from exceptions.kubernetes_exception import KubernetesException
from exceptions.repo_manager_exception import RepositoryManagerException
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError
import logging


# Configure logger
logger = logging.getLogger(__name__)


class RLAgent:
    """
    A Reinforcement Learning agent.
    """

    def __init__(self, kubernetes_conn, repo_manager_conn, name, pod_name, min_replicas=0, max_replicas=1):
        """
        Create a new Reinforcement Learning agent.
        :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
        :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
        :param name: (string) the Smart Scaler name.
        :param pod_name: (string) the Pod name.
        :param min_replicas: (integer) the minimum replication degree (default is 0).
        :param max_replicas: (integer) the maximum replication degree (default is 1).
        """
        self.kubernetes_conn = kubernetes_conn
        self.repo_manager_conn = repo_manager_conn

        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas

        self.last_pod_status = None

    def create_learning_context(self):
        """
        Create the learning context within the repository.
        :return: (void)
        """
        learning_parameters = {
            "min_replicas": self.min_replicas,
            "max_replicas": self.max_replicas,
            "alpha": 0.5,
            "gamma": 0.5
        }

        try:
            repo_manager_ctrl.create_learning_context(self.repo_manager_conn, self.name, learning_parameters)
        except ConnectionError as exc:
            logger.warning("Cannot connect to Repository Manager: {}".format(str(exc)))
            return False
        except JSONDecodeError as exc:
            logger.warning("Malformed response from Repository Manager: {}".format(str(exc)))
            return False
        except RepositoryManagerException as exc:
            if exc.code is 404:
                logger.warning("Error from Repository Manager: {}".format(exc.message))
                return True
            else:
                logger.warning("Error from Repository Manager: {}".format(exc.message))


        return True

    def remove_learning_context(self):
        """
        Remove the learning context within the repository.
        :return: (void)
        """
        try:
            repo_manager_ctrl.remove_learning_context(self.repo_manager_conn, self.name)
        except ConnectionError as exc:
            logger.warning("Cannot connect to Repository Manager: {}".format(str(exc)))
            return False
        except JSONDecodeError as exc:
            logger.warning("Malformed response from Repository Manager: {}".format(str(exc)))
            return False
        except RepositoryManagerException as exc:
            logger.warning("Error from Repository Manager: {}".format(exc.message))
            return False

        return True

    def has_context(self):
        """
        Check whether the agent has an already initialized learning context.
        :return: True, if agent has an already initialized learning context; False, otherwise.
        """
        return repo_manager_ctrl.has_learning_context(self.repo_manager_conn, self.name)

    def apply_scaling_action(self):
        """
        Apply the scaling action, connecting to Kubernetes and Repo Manager.
        :return: (void)
        """
        pod_name = self.pod_name
        try:
            pod_status = kubernetes_ctrl.get_pod_status(self.kubernetes_conn, self.pod_name)
            learning_context = repo_manager_ctrl.get_learning_context(self.repo_manager_conn, self.pod_name)
            reward = self._compute_reward(pod_status)
            suggested_replicas = self._compute_replicas(pod_status, reward, learning_context)

            current_replicas = pod_status["replicas"]
            if current_replicas != suggested_replicas:
                replicas_old, replicas_new = kubernetes_ctrl.set_pod_replicas(self.kubernetes_conn, pod_name, suggested_replicas)
                logger.info("Pod {} scaled from {} to {}".format(pod_name, replicas_old, replicas_new))
            else:
                logger.info("Pod {} not scaled ({} replicas)".format(pod_name, current_replicas))

            self.last_pod_status = pod_status
        except ConnectionError as exc:
            logger.warning("Cannot connect to Kubernetes: {}".format(str(exc)))
        except JSONDecodeError as exc:
            logger.warning("Malformed response from Kubernetes: {}".format(str(exc)))
            return
        except KubernetesException as exc:
            logger.warning("Error from Kubernetes: {}".format(exc.message))

    def _compute_reward(self, pod_status):
        """
        Compute the reward.
        :param pod_status: the current Pod state.
        :return: (float) the reward.
        """
        cpu_utilization_curr = pod_status["cpu_utilization"]
        cpu_utilization_prev = self.last_pod_status["cpu_utilization"] if self.last_pod_status is not None else 0.0
        return (cpu_utilization_curr - cpu_utilization_prev)

    def _compute_replicas(self, pod_status, reward, learning_context):
        """
        Compute the replication degree.
        :param pod_status: (PodState) the current Pod state.
        :param reward: (float) the current reward.
        :param learning_context: (LearningParams) the current learning context.
        :return: the suggested replication degree.
        """
        cpu_utilization = pod_status["cpu_utilization"]

        q_matrix = learning_context["matrix"]

        if 0.0 <= cpu_utilization <= 0.40:
            suggested_replicas = self.min_replicas
        elif 0.40 < cpu_utilization <= 0.80:
            suggested_replicas = self.min_replicas + self.max_replicas
        else:
            suggested_replicas = self.max_replicas

        return suggested_replicas

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "Agent({},{} @ {},{})".format(self.name, self.pod_name, self.min_replicas, self.max_replicas, self.kubernetes_conn, self.repo_manager_conn)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()
