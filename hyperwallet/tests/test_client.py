#!/usr/bin/env python

import mock
import json
import unittest

from hyperwallet.utils import ApiClient
from hyperwallet.config import SERVER
from hyperwallet.exceptions import HyperwalletAPIException


class ApiClientTest(unittest.TestCase):

    def setUp(self):

        self.client = ApiClient(
            'test-user',
            'test-pass',
            SERVER
        )

    def test_failed_connection(self):

        with self.assertRaises(HyperwalletAPIException) as exc:
            self.client._makeRequest()

        self.assertEqual(
            exc.exception.message.get('errors')[0].get('code'),
            'COMMUNICATION_ERROR'
        )

    @mock.patch('requests.Session.request')
    def test_receive_valid_json_empty_response(self, session_mock):

        session_mock.return_value = mock.MagicMock(
            status_code=204
        )

        self.assertEqual(self.client._makeRequest(), {})

    @mock.patch('requests.Session.request')
    def test_receive_non_json_response(self, session_mock):

        data = '<html>404</html>'

        session_mock.return_value = mock.MagicMock(
            status_code=404,
            content=data
        )

        with self.assertRaises(HyperwalletAPIException) as exc:
            self.client._makeRequest()

        self.assertEqual(
            exc.exception.message.get('errors')[0].get('code'),
            'GARBAGE_RESPONSE'
        )

    @mock.patch('requests.Session.request')
    def test_receive_valid_json_error_response(self, session_mock):

        data = {
            "errors": [{
                "message": "Houston, we have a problem",
                "code": "FORBIDDEN"
            }]
        }

        session_mock.return_value = mock.MagicMock(
            status_code=400,
            content=json.dumps(data)
        )

        with self.assertRaises(HyperwalletAPIException) as exc:
            self.client._makeRequest()

        self.assertEqual(
            exc.exception.message.get('errors')[0].get('code'),
            'FORBIDDEN'
        )

    @mock.patch('requests.Session.request')
    def test_receive_valid_json_response(self, session_mock):

        data = {
            'key': 'value'
        }

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=json.dumps(data)
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.client._makeRequest(),
            json.loads(encoded)
        )


if __name__ == '__main__':
    unittest.main()
