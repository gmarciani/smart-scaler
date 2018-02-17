from services.common.model.ai.smart_scaling import smart_scaler_factory
from services.common.model.resources.smart_scaler_resource import SmartScalerResource
from services.common.model.resources.pod_resource import PodResource
from services.common.model.ai.smart_scaling.smart_scaling_agent import SmartScalerQLearning
from services.common.model.ai.qlearning.qlearning_agent import QLearningAgent as QLearningAgent
from services.common.model.ai.smart_scaling import rewarding as rewarding_functions
from services.common.model.ai.smart_scaling.actions import SimpleScalingAction as ScalingAction
from services.common.model.ai.smart_scaling import actions_utils
from services.common.model.ai.smart_scaling import states
import random
import unittest


class SmartScalingAgentTestCase(unittest.TestCase):

    def test_binary_serialization(self):
        """
        Test the binary serialization.
        :return: None
        """
        name = "ss_my_pod"
        podname = "my_pod"
        min_replicas = 1
        max_replicas = 5
        granularity = 5
        rewarding_function = rewarding_functions.simple_rewarding

        iterations = 100

        agent = QLearningAgent(
            states=states.ReplicationUtilizationSpace(min_replicas, max_replicas, granularity),
            actions=actions_utils.generate_action_space(ScalingAction),
            rewarding_function=rewarding_function)

        print("States: ", agent.states)
        print("Actions: ", agent.actions)

        scaler = SmartScalerQLearning(name, podname, min_replicas, max_replicas, agent)

        actual = SmartScalerQLearning.from_binarys(scaler.to_binarys())
        expected = scaler
        self.assertEqual(expected, actual, "Binary serialization error")

        pod = PodResource(podname, min_replicas)

        for i in range(iterations):

            pod.cpu_utilization = random.random()

            curr_state = scaler.map_state(pod.replicas, pod.cpu_utilization)

            new_replicas, action = scaler.get_replicas(curr_state, return_action=True)

            pod.replicas = new_replicas

            scaler.save_experience(curr_state, action)

        actual = SmartScalerQLearning.from_binarys(scaler.to_binarys())
        expected = scaler
        self.assertEqual(expected, actual, "Binary serialization error")

    def test_learning(self):
        """
        Test the learning loop.
        :return:
        """
        try:
            name = "ss_my_pod"
            podname = "my_pod"
            min_replicas = 1
            max_replicas = 5
            granularity = 5
            round = None
            alpha = 0.5
            gamma = 0.9
            epsilon = 0.1
            rewarding_function = rewarding_functions.simple_rewarding

            iterations = 100

            smart_scaler_resource = SmartScalerResource(
                name="ss-pod-1",
                pod_name="pod-1",
                min_replicas=1,
                max_replicas=10,
                ai_technique="QLEARNING"
            )

            agent = QLearningAgent(
                states=states.ReplicationUtilizationSpace(min_replicas, max_replicas, granularity, round),
                actions=actions_utils.generate_action_space(ScalingAction),
                alpha=alpha, gamma=gamma, epsilon=epsilon,
                rewarding_function=rewarding_function)

            smart_scaler = smart_scaler_factory.create(smart_scaler_resource)

            pod = PodResource(podname, min_replicas)

            for i in range(iterations):

                pod.cpu_utilization = random.random()

                curr_state = smart_scaler.map_state(pod.replicas, pod.cpu_utilization)

                new_replicas, action = smart_scaler.get_replicas(curr_state, return_action=True)

                pod.replicas = new_replicas

                smart_scaler.save_experience(curr_state, action)
        except Exception as exc:
            self.fail("Error during learning loop: {}".format(exc))


if __name__ == "__main__":
    unittest.main()
