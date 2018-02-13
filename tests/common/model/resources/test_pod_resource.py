from services.common.model.resources.pod_resource import PodResource as PodResource
import unittest


class PodResourceTestCase(unittest.TestCase):

    def test_jsons(self):
        """
        Test the JSON serialization.
        :return:
        """
        pod = PodResource("pod-1")

        actual = PodResource.from_jsons(pod.to_jsons())

        expected = pod
        self.assertEqual(expected, actual, "JSON serialization error")

    def test_json(self):
        """
        Test the JSON object conversion.
        :return:
        """
        pod = PodResource("pod-1")

        actual = PodResource.from_json(pod.to_json())

        expected = pod
        self.assertEqual(expected, actual, "JSON conversion error")


if __name__ == "__main__":
    unittest.main()
