import unittest
from services.redis_simulator.app import app


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_empty_db(self):
        rv = self.app.get("/status")
        assert b"OK" in rv.data


if __name__ == "__main__":
    unittest.main()