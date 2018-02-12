from services.common.model.resources.smart_scaler import SmartScalerResource
from services.common.model.resources.pod import PodResource
from services.kubernetes_simulator.app import app as app
from tests.common import responses
from tests.common.requests import to_json as to_json
import unittest


class RegistrySmartScalersTestCase(unittest.TestCase):

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
        Test the CRUD of smart scalers.
        :return:
        """
        smart_scaler = SmartScalerResource("my-smart-scaler-1", "my-pod-1")
        pod = PodResource("my-pod-1")

        # Retrieve all (empty)
        rv = self.app.get("/registry/smart_scalers")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(smart_scalers=[])
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Create (not existing pod)
        rv = self.app.put("/registry/smart_scalers", data=to_json(smart_scaler), content_type="application/json")
        self.assertEqual(400, rv.status_code, "HTTP status code mismatch")

        # Create pod
        rv = self.app.put("/registry/pods", data=to_json(pod), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(pod=vars(pod))
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Create
        rv = self.app.put("/registry/smart_scalers", data=to_json(smart_scaler), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(smart_scaler=vars(smart_scaler))
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Create existing
        rv = self.app.put("/registry/smart_scalers", data=to_json(smart_scaler), content_type="application/json")
        self.assertEqual(400, rv.status_code, "HTTP status code mismatch")

        # Retrieve
        rv = self.app.get("/registry/smart_scalers", query_string=dict(name=smart_scaler.name))
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(smart_scaler=vars(smart_scaler))
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Retrieve all
        rv = self.app.get("/registry/smart_scalers")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(smart_scalers=[vars(smart_scaler)])
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Delete existing
        rv = self.app.delete("/registry/smart_scalers", data=to_json(dict(name=smart_scaler.name)), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(smart_scaler=vars(smart_scaler))
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Retrieve non existing
        rv = self.app.get("/registry/smart_scalers", query_string=dict(name=smart_scaler.name))
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")

        # Delete non existing
        rv = self.app.delete("/registry/smart_scalers", data=to_json(dict(name=smart_scaler.name)), content_type="application/json")
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")


if __name__ == "__main__":
    unittest.main()
