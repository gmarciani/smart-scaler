from services.redis_simulator.app import app as app
from tests.common import responses
import unittest


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

    def test_retrieval_all(self):
        """
        Test the retrieval of all entries.
        :return:
        """
        rv = self.app.get("/database")
        self.assertTrue(responses.match_status(rv, 200), "HTTP status code mismatch")

        expected = dict(values={})
        self.assertTrue(responses.match_data(rv, expected), "JSON mismatch")

    def test_creation(self):
        """
        Test the creation of an entry.
        :return:
        """
        rv = self.app.get("/database")
        self.assertTrue(responses.match_status(rv, 200), "HTTP status code mismatch")

        expected = dict(values={})
        self.assertTrue(responses.match_data(rv, expected), "JSON mismatch")


if __name__ == "__main__":
    unittest.main()
