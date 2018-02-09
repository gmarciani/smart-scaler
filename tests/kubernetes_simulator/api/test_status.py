from services.kubernetes_simulator.app import app as app
from tests.common import responses
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

        expected = dict(status="OK")
        self.assertTrue(responses.match_data(rv, expected), "JSON mismatch")


if __name__ == "__main__":
    unittest.main()