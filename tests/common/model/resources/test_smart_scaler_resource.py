from services.common.model.resources.smart_scaler_resource import SmartScalerResource as SmartScalerResource
import unittest


class SmartScalerResourceTestCase(unittest.TestCase):

    def test_jsons(self):
        """
        Test the JSON serialization.
        :return:
        """
        smart_scaler_resource = SmartScalerResource(
            name="ss-pod-1",
            pod_name="pod-1",
            min_replicas=1,
            max_replicas=10,
            ai_technique="QLEARNING_RND"
        )

        actual = SmartScalerResource.from_jsons(smart_scaler_resource.to_jsons())

        expected = smart_scaler_resource
        self.assertEqual(expected, actual, "JSON serialization error")

        smart_scaler_resource = SmartScalerResource(
            name="ss-pod-1",
            pod_name="pod-1",
            min_replicas=1,
            max_replicas=10,
            ai_technique="QLEARNING",
            state_granularity=10,
            state_precision=5,
            action_magnitude=1,
            alpha=0.5,
            gamma=0.9,
            epsilon=0.1
        )

        actual = SmartScalerResource.from_jsons(smart_scaler_resource.to_jsons())

        expected = smart_scaler_resource
        self.assertEqual(expected, actual, "JSON serialization error")

    def test_json(self):
        """
        Test the JSON object conversion.
        :return:
        """
        smart_scaler_resource = SmartScalerResource(
            name="ss-pod-1",
            pod_name="pod-1",
            min_replicas=1,
            max_replicas=10,
            ai_technique="QLEARNING_RND"
        )

        actual = SmartScalerResource.from_json(smart_scaler_resource.to_json())

        expected = smart_scaler_resource
        self.assertEqual(expected, actual, "JSON conversion error")

        smart_scaler_resource = SmartScalerResource(
            name="ss-pod-1",
            pod_name="pod-1",
            min_replicas=1,
            max_replicas=10,
            ai_technique="QLEARNING",
            state_granularity=10,
            state_precision=5,
            action_magnitude=1,
            alpha=0.5,
            gamma=0.9,
            epsilon=0.1
        )

        actual = SmartScalerResource.from_json(smart_scaler_resource.to_json())

        expected = smart_scaler_resource
        self.assertEqual(expected, actual, "JSON conversion error")


if __name__ == "__main__":
    unittest.main()
