import unittest
from services.api_gateway.app import app


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_status(self):
        rv = self.app.get("/status")
        assert b"OK" in rv.data


if __name__ == "__main__":
    unittest.main()