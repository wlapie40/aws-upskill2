import unittest
from src import app


class TestHello(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        # self.assertEqual(rv.data, b'Hello World!\n')

    def test_create_bucket(self):
        rv = self.app.get('/create_bucket')
        self.assertEqual(rv.status, '200 OK')
        # self.assertEqual(rv.data, b'Hello World!\n')

    def test_cloud_watch(self):
        rv = self.app.get(f'/instance/monitoring')
        self.assertEqual(rv.status, '200 OK')
        # self.assertIn(bytearray(f"{name}", 'utf-8'), rv.data)


if __name__ == '__main__':
    unittest.main()