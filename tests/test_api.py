import unittest
from urllib import response
import pytest

from api.app import app


class TestMainRoute(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
    def test_success_main_route(self):
        response = self.app.get('/')
        self.assertEqual(b'{"api-key-version": "0.0.1"}\n', response.data)

