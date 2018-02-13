from services.common.model.resources.smart_scaler import SmartScalerResource as SmartScalerResource
import unittest


class SmartScalerResourceTestCase(unittest.TestCase):

    def test_json(self):
        """
        Test the JSON serialization.
        :return:
        """
        smart_scaler = SmartScalerResource("my-smart-scaler-1", "my-pod-1")

        actual = SmartScalerResource.from_jsons(smart_scaler.to_jsons())

        expected = smart_scaler
        self.assertEqual(expected, actual, "JSON serialization error")


if __name__ == "__main__":
    unittest.main()
