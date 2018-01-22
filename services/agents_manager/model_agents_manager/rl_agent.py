from control_agents_manager import kubernetes_simulation as kubernetes_ctrl
from control_agents_manager import repo_manager as repo_manager_ctrl
from control_agents_manager import qlearning as qlearning_ctrl
from exceptions.kubernetes_exception import KubernetesException
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError
import logging


# Configure logger
logger = logging.getLogger(__name__)


class RLAgent:
    """
    A Reinforcement Learning agent.
    """

    def __init__(self, kubernetes_conn, repo_manager_conn, name, pod_name, min_replicas=0, max_replicas=1, state_granularity=10):
        """
        Create a new Reinforcement Learning agent.
        :param kubernetes_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
        :param repo_manager_conn: (tuple:(string,int)) the Kubernetes connection (host,port).
        :param name: (string) the Smart Scaler name.
        :param pod_name: (string) the Pod name.
        :param min_replicas: (integer) the minimum replication degree (default is 0).
        :param max_replicas: (integer) the maximum replication degree (default is 1).
        :param state_granularity: (integer) the granularity level (default is 10).
        """
        self.kubernetes_conn = kubernetes_conn
        self.repo_manager_conn = repo_manager_conn

        self.name = name
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.state_granularity = state_granularity

        self.last_state = None
        self.last_action = None

    def create_learning_context(self):
        """
        Create the learning context within the repository.
        :return: (void)
        """
        context_parameters = {
            "pod_name": self.pod_name,
            "alpha": 0.5,
            "gamma": 0.5,
            "state_granularity": 10
        }

        repo_manager_ctrl.create_learning_context(self.repo_manager_conn, self.name, context_parameters)

    def remove_learning_context(self):
        """
        Remove the learning context within the repository.
        :return: (void)
        """
        repo_manager_ctrl.remove_learning_context(self.repo_manager_conn, self.name)

    def has_learning_context(self):
        """
        Check whether the agent has an already initialized learning context.
        :return: True, if agent has an already initialized learning context; False, otherwise.
        """
        return repo_manager_ctrl.exists_learning_context(self.repo_manager_conn, self.name)

    def apply_scaling_action(self):
        """
        Apply the scaling action, connecting to Kubernetes and Repo Manager.
        :return: (void)
        """
        pod_name = self.pod_name
        try:
            # Retrieve the learning context
            learning_context = repo_manager_ctrl.get_learning_context(self.repo_manager_conn, self.name)

            # Compute reward
            pod_state = kubernetes_ctrl.get_pod_status(self.kubernetes_conn, self.pod_name)
            reward = qlearning_ctrl.compute_reward(pod_state, self.last_state)

            # Update matrix
            matrix = learning_context["matrix"]
            normalized_state = qlearning_ctrl.compute_normalized_state(pod_state)
            matrix_state = min(self.state_granularity -1, int(normalized_state * self.state_granularity))
            matrix[matrix_state][self.last_action.value] = reward

            # Compute action
            action = qlearning_ctrl.compute_action(pod_state, matrix)

            # Execute action
            current_replicas = pod_state["replicas"]
            scale_amount = 1 if action is qlearning_ctrl.Action.SCALE_OUT else (-1 if action is qlearning_ctrl.Action.SCALE_IN else 0)
            suggested_replicas = current_replicas + scale_amount
            if current_replicas != suggested_replicas:
                replicas_old, replicas_new = kubernetes_ctrl.set_pod_replicas(self.kubernetes_conn, pod_name, suggested_replicas)
                logger.info("Pod {} scaled from {} to {}".format(pod_name, replicas_old, replicas_new))
            else:
                logger.info("Pod {} not scaled ({} replicas)".format(pod_name, current_replicas))

            # Update agent state
            self.last_state = pod_state
            self.last_action = action

            # Backup matrix on repository
            learning_context["matrix"] = matrix
            repo_manager_ctrl.update_learning_context(self.repo_manager_conn, self.name, learning_context)

        except ConnectionError as exc:
            logger.warning("Cannot connect to Kubernetes: {}".format(str(exc)))
        except JSONDecodeError as exc:
            logger.warning("Malformed response from Kubernetes: {}".format(str(exc)))
            return
        except KubernetesException as exc:
            logger.warning("Error from Kubernetes: {}".format(exc.message))

    def __str__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return "Agent({},{},{},{},{},{})".format(self.name, self.pod_name, self.min_replicas, self.max_replicas, self.kubernetes_conn, self.repo_manager_conn)

    def __repr__(self):
        """
        Return the string representation.
        :return: (string) the string representation.
        """
        return self.__str__()
