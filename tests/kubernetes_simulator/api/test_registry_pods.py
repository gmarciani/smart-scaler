from services.common.model.resources.pod_resource import PodResource
from services.kubernetes_simulator.app import app as app
from tests.test_utils import responses
from tests.test_utils.requests import to_json as to_json
import unittest
from copy import deepcopy


class RegistryPodsTestCase(unittest.TestCase):

    def setUp(self):
        """
        Setup the application.
        :return: None
        """
        self.app = app.test_client()

    def tearDown(self):
        """
        Teardown the application.
        :return: None
        """
        pass

    def test_crud(self):
        """
        Test the CRUD of pods.
        :return:
        """
        pod = PodResource("pod-1")

        # Retrieve all (empty)
        rv = self.app.get("/registry/pods")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pods=[])
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Create
        rv = self.app.put("/registry/pods", data=pod.to_jsons(), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pod=pod.to_json())
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Create existing
        rv = self.app.put("/registry/pods", data=pod.to_jsons(), content_type="application/json")
        self.assertEqual(400, rv.status_code, "HTTP status code mismatch")

        # Retrieve
        rv = self.app.get("/registry/pods", query_string=dict(name=pod.name))
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pod=pod.to_json())
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Retrieve all
        rv = self.app.get("/registry/pods")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pods=[pod.to_json()])
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Update
        pod_old = deepcopy(pod)
        pod = PodResource(pod.name, pod.replicas * 2)
        rv = self.app.patch("/registry/pods", data=pod.to_jsons(), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pod=pod.to_json(), pod_old=pod_old.to_json())
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Retrieve (updated)
        rv = self.app.get("/registry/pods", query_string=dict(name=pod.name))
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pod=pod.to_json())
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Delete existing
        rv = self.app.delete("/registry/pods", data=to_json(dict(name=pod.name)), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pod=pod.to_json(), smart_scalers=None)
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Update non existing
        pod_old = deepcopy(pod)
        pod = PodResource(pod.name, pod.replicas * 2)
        rv = self.app.patch("/registry/pods", data=pod.to_jsons(), content_type="application/json")
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")

        # Retrieve non existing
        rv = self.app.get("/registry/pods", query_string=dict(name=pod.name))
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")

        # Delete non existing
        rv = self.app.delete("/registry/pods", data=to_json(dict(name=pod.name)), content_type="application/json")
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")


if __name__ == "__main__":
    unittest.main()
