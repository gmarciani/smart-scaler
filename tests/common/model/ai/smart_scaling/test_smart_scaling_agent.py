from services.common.model.ai.smart_scaling import smart_scaler_factory
from services.common.model.resources.smart_scaler_resource import SmartScalerResource
from services.common.model.resources.pod_resource import PodResource
from services.common.model.ai.smart_scaling.smart_scaling_agent import SmartScalerQLearning
import random
import unittest


class SmartScalingAgentTestCase(unittest.TestCase):


    def test_creation(self):
        """
        Test the creation of a Smart Scaler.
        :return: None.
        """
        smart_scaler_resource = SmartScalerResource(
            name="ss-pod-1",
            pod_name="pod-1",
            min_replicas=1,
            max_replicas=10,
            ai_technique="QLEARNING",
            rewarding_function="reward_naive",
            state_granularity=10,
            state_precision=5,
            action_magnitude=3,
            alpha=0.5,
            gamma=0.9,
            epsilon=0.1
        )

        scaler = smart_scaler_factory.create(smart_scaler_resource)

        print(scaler)
        print(scaler.pretty())


    def test_binary_serialization(self):
        """
        Test the binary serialization.
        :return: None
        """
        smart_scaler_resource = SmartScalerResource(
            name="ss-pod-1",
            pod_name="pod-1",
            min_replicas=1,
            max_replicas=10,
            ai_technique="QLEARNING",
            rewarding_function="reward_naive",
            state_granularity=10,
            state_precision=5,
            action_magnitude=3,
            alpha=0.5,
            gamma=0.9,
            epsilon=0.1
        )

        scaler = smart_scaler_factory.create(smart_scaler_resource)

        actual = SmartScalerQLearning.from_binarys(scaler.to_binarys())
        expected = scaler
        self.assertEqual(expected, actual, "Binary serialization error")

        pod = PodResource("pod-1")

        for i in range(100):

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
            smart_scaler_resource = SmartScalerResource(
                name="ss-pod-1",
                pod_name="pod-1",
                min_replicas=1,
                max_replicas=10,
                ai_technique="QLEARNING",
                rewarding_function="reward_naive",
                state_granularity=10,
                state_precision=5,
                action_magnitude=3,
                alpha=0.5,
                gamma=0.9,
                epsilon=0.1
            )

            smart_scaler = smart_scaler_factory.create(smart_scaler_resource)

            pod = PodResource("pod-1")

            for i in range(100):

                pod.cpu_utilization = random.random()

                curr_state = smart_scaler.map_state(pod.replicas, pod.cpu_utilization)

                new_replicas, action = smart_scaler.get_replicas(curr_state, return_action=True)

                pod.replicas = new_replicas

                smart_scaler.save_experience(curr_state, action)
        except Exception as exc:
            self.fail("Error during learning loop: {}".format(exc))


if __name__ == "__main__":
    unittest.main()
