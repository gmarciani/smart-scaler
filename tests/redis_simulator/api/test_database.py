from services.redis_simulator.app import app as app
from tests.test_utils import responses
import unittest
import json


class DatabaseTestCase(unittest.TestCase):

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
        Test the CRUD of entries.
        :return:
        """
        key = "key_1"
        value = "val_1"

        # Retrieve all (empty)
        rv = self.app.get("/database")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        values_actual = responses.get_data_field(rv, "values")
        values_expected = dict()
        self.assertEqual(values_expected, values_actual, "Value mismatch")

        # Create
        rv = self.app.post("/database", data=json.dumps(dict(key=key, value=value)), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(key=key, value=value, value_old=None)
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Create existing
        rv = self.app.post("/database", data=json.dumps(dict(key=key, value=value, unique=True)), content_type="application/json")
        self.assertEqual(400, rv.status_code, "HTTP status code mismatch")

        # Retrieve
        rv = self.app.get("/database", query_string=dict(key=key))
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(key=key, value=value)
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Retrieve all
        rv = self.app.get("/database")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(values={key: value})
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Update
        value_old = value
        value = "val_1_new"
        rv = self.app.patch("/database", data=json.dumps(dict(key=key, value=value)), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(key=key, value=value, value_old=value_old)
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Retrieve (updated)
        rv = self.app.get("/database", query_string=dict(key=key))
        self.assertTrue(responses.match_status(rv, 200), "HTTP status code mismatch")

        expected = dict(key=key, value=value)
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Delete existing
        rv = self.app.delete("/database", data=json.dumps(dict(key=key)), content_type="application/json")
        self.assertEqual(200, rv.status_code, "HTTP status code mismatch")

        expected = dict(key=key, value=value)
        self.assertDictEqual(expected, responses.get_json(rv), "JSON mismatch")

        # Update non existing
        rv = self.app.patch("/database", data=json.dumps(dict(key=key, value=value)), content_type="application/json")
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")

        # Retrieve non existing
        rv = self.app.get("/database", query_string=dict(key=key))
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")

        # Delete non existing
        rv = self.app.delete("/database", data=json.dumps(dict(key=key)), content_type="application/json")
        self.assertEqual(404, rv.status_code, "HTTP status code mismatch")


if __name__ == "__main__":
    unittest.main()
