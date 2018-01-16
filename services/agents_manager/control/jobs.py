from control import kube
from datetime import datetime
from model.rl_agent import RLAgent


def main_loop(kube_host, kube_port, agents):
    """
    Update agents and apply scaling actions on Kubernetes.
    :param kube_host: (string) the Kubernetes hostname.
    :param kube_port: (int) the Kubernetes port.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    _update_agents(kube_host, kube_port, agents)
    print("[UPDATED] Agents: ", agents)
    _apply_scaling_actions(kube_host, kube_port, agents)


def _update_agents(kube_host, kube_port, agents):
    """
    Update agents pulling currently active Smart Scalers on Kubernetes.
    :param kube_host: (string) the Kubernetes hostname.
    :param kube_port: (int) the Kubernetes port.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    smart_scalers = kube.get_all_kube_smart_scalers(kube_host, kube_port)

    if smart_scalers is None:
        print("{} || smart_scalers is None".format(datetime.now()))
        return None

    smart_scalers_to_remove = list(agents.keys() - set(map(lambda x: x["name"], smart_scalers)))

    smart_scalers_to_add = list(filter(lambda x: x["name"] not in agents, smart_scalers))

    for smart_scaler_name in smart_scalers_to_remove:
        del agents[smart_scaler_name]

    for smart_scaler in smart_scalers_to_add:
        agent_new = RLAgent(
            smart_scaler["name"],
            smart_scaler["pod_name"],
            smart_scaler["min_replicas"] | 1,
            smart_scaler["max_replicas"] | 10
        )
        agents[smart_scaler["name"]] = agent_new


def _apply_scaling_actions(kube_host, kube_port, agents):
    """
    Apply scaling actions provided by agents.
    :param kube_host: (string) the Kubernetes hostname.
    :param kube_port: (int) the Kubernetes port.
    :param agents: (dict) the repository of agents ({smart_scaler_name: agent}).
    :return: (void)
    """
    for agent in agents.values():
        pod_name = agent.pod_name
        pod_status = kube.get_pod_status(kube_host, kube_port, pod_name)
        new_replicas = agent.compute_replicas(pod_status)
        success = kube.set_pod_replicas(kube_host, kube_port, pod_name, new_replicas)
        print("Pod {} scaled from {} to {}: {}".format(pod_name, pod_status["replicas"], new_replicas, success))


def shutdown_hook(param):
    """
    Perform all shutdown actions.
    :param param: (dict) dictionary of parameters.
    :return: (void)
    """
    print("Shutdown Hook at {}: {}", datetime.now(), param)