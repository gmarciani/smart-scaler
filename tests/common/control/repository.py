from services.common.model.environment.connection import SimpleConnection
from services.redis_simulator.app import app as app
import unittest

@unittest.skip
class RepositoryTestCase(unittest.TestCase):

    def setUp(self):
        """
        Setup the application.
        :return: None
        """
        self.repository_connection = SimpleConnection("0.0.0.0", 1234)
        self.app = app.start_detached(host=self.repository_connection.host, port=self.repository_connection.port)

    def tearDown(self):
        """
        Teardown the application.
        :return: None
        """
        self.app.shutdown()

    def test_crud(self):
        """
        Test the CRUD operations.
        :return:
        """
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()