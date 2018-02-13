from services.common.model.resources.pod import PodResource as PodResource
import unittest


class PodResourceTestCase(unittest.TestCase):

    def test_json(self):
        """
        Test the JSON serialization.
        :return:
        """
        pod = PodResource("my-pod-1")

        actual = PodResource.from_jsons(pod.to_jsons())

        expected = pod
        self.assertEqual(expected, actual, "JSON serialization error")


if __name__ == "__main__":
    unittest.main()
