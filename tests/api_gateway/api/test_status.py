from services.api_gateway.app import app
from tests.test_utils import responses

import unittest


class StatusTestCase(unittest.TestCase):

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

    def test_status_get(self):
        """
        Test the REST interface 'GET /status'
        :return:
        """
        rv = self.app.get("/status")
        self.assertTrue(responses.match_status(rv, 200), "HTTP status code mismatch")

        expected_1 = dict(status="OK")
        expected_2 = dict(status="FAILED")
        self.assertTrue(responses.match_data(rv, expected_1) or responses.match_data(rv, expected_2), "JSON mismatch")


if __name__ == "__main__":
    unittest.main()