import os
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

import cronitor

# a reserved monitorId for running integration tests against cronitor.link
FAKE_ID = 'd3x0c1'
FAKE_PING_API_KEY = 'ping-api-key'

class MonitorPingTests(unittest.TestCase):

    def test_endpoints(self):
        monitor = cronitor.Monitor(id=FAKE_ID)
        endpoints = ['run', 'complete', 'tick', 'fail', 'ok']

        for endpoint in endpoints:
            resp = monitor.__getattribute__(endpoint)()
            self.assertEqual(resp.status_code, 200)

    def test_ping_api_key(self):
        monitor = cronitor.Monitor(id=FAKE_ID, ping_api_key=FAKE_PING_API_KEY)
        self.assertDictContainsSubset({'auth_key': FAKE_PING_API_KEY}, monitor._clean_params({}))

    def test_message(self):
        monitor = cronitor.Monitor(id=FAKE_ID)
        message = 'a test message'
        self.assertDictContainsSubset({'msg': message}, monitor._clean_params({'message': message}))

    def test_environment_param(self):
        cronitor.environment = 'development'
        monitor = cronitor.Monitor(id=FAKE_ID)
        self.assertDictContainsSubset({'env': 'development'}, monitor._clean_params({}))

    @patch('cronitor.Monitor._ping')
    def test_all_params_sent(self, ping):
        monitor = cronitor.Monitor(id=FAKE_ID)
        monitor.run(**{
            'message': "test",
            'env': 'staging',
            'duration': 1,
            'host': 'blue-oyster',
            'series': 'a.b.c',
            'count': '42',
            'error_count': 0})

        ping.assert_called_once_with('run', {
            'message': "test",
            'env': 'staging',
            'duration': 1,
            'host': 'blue-oyster',
            'series': 'a.b.c',
            'count': '42',
            'error_count': 0 })



