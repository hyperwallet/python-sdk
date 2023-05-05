#!/usr/bin/env python

import mock
import json
import unittest
import os.path

from hyperwallet.utils import ApiClient
from hyperwallet.config import SERVER
from hyperwallet.exceptions import HyperwalletAPIException
from hyperwallet.utils.encryption import Encryption


class ApiClientTest(unittest.TestCase):

    def setUp(self):

        self.client = ApiClient(
            'test-user',
            'test-pass',
            SERVER
        )

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')

        self.clientWithEncryption = ApiClient(
            'test-user',
            'test-pass',
            SERVER,
            {'clientPrivateKeySetLocation': clientPath, 'hyperwalletKeySetLocation': hyperwalletPath}
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
            content=data,
            headers={
                "Content-Type": "application/json"
            }
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
                "code": "FORBIDDEN",
                "relatedResources": ["trm-f3d38df1-adb7-4127-9858-e72ebe682a79", "trm-601b1401-4464-4f3f-97b3-09079ee7723b"]
            }]
        }

        session_mock.return_value = mock.MagicMock(
            status_code=400,
            content=json.dumps(data),
            headers={
                "Content-Type": "application/json"
            }
        )

        with self.assertRaises(HyperwalletAPIException) as exc:
            self.client._makeRequest()

        self.assertEqual(
            exc.exception.message.get('errors')[0].get('code'),
            'FORBIDDEN'
        )

        self.assertEqual(
            exc.exception.message.get('errors')[0].get('relatedResources')[0],
            'trm-f3d38df1-adb7-4127-9858-e72ebe682a79'
        )

        self.assertEqual(
            exc.exception.message.get('errors')[0].get('relatedResources')[1],
            'trm-601b1401-4464-4f3f-97b3-09079ee7723b'
        )

    @mock.patch('requests.Session.request')
    def test_receive_valid_json_response(self, session_mock):

        data = {
            'key': 'value'
        }

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=json.dumps(data),
            headers={
                "Content-Type": "application/json"
            }
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.client._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_request_with_encryption_successful(self, session_mock):

        data = {
            'key': 'value'
        }

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        encryptedMessage = encryption.encrypt(json.dumps(data))

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=encryptedMessage,
            headers={
                "Content-Type": "application/jose+json"
            }
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.clientWithEncryption._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_request_with_encryption_when_content_type_contains_charset(self, session_mock):

        data = {
            'key': 'value'
        }

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        encryptedMessage = encryption.encrypt(json.dumps(data))

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=encryptedMessage,
            headers={
                "Content-Type": "application/jose+json;charset=utf-8"
            }
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.clientWithEncryption._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_request_with_encryption_when_content_type_contains_charset_ahead(self, session_mock):

        data = {
            'key': 'value'
        }

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        encryptedMessage = encryption.encrypt(json.dumps(data))

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=encryptedMessage,
            headers={
                "Content-Type": "charset=utf-8;application/jose+json"
            }
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.clientWithEncryption._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_request_with_encryption_when_response_content_type_is_not_valid(self, session_mock):

        data = {
            'key': 'value'
        }

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        encryptedMessage = encryption.encrypt(json.dumps(data))

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=encryptedMessage,
            headers={
                "Content-Type": "wrongContentType"
            }
        )

        with self.assertRaises(HyperwalletAPIException) as exc:
            self.clientWithEncryption._makeRequest()

        self.assertEqual(
            exc.exception.message,
            'Invalid Content-Type specified in Response Header'
        )

    @mock.patch('requests.Session.request')
    def test_request_with_encryption_when_status_code_204_and_content_type_is_not_set(self, session_mock):

        data = {}

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        encryptedMessage = encryption.encrypt(json.dumps(data))

        session_mock.return_value = mock.MagicMock(
            status_code=204,
            content=encryptedMessage,
            headers={}
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.clientWithEncryption._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_receive_valid_json_response_when_content_type_contains_charset(self, session_mock):

        data = {
            'key': 'value'
        }

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=json.dumps(data),
            headers={
                "Content-Type": "application/json;charset=utf-8"
            }
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.client._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_receive_valid_json_response_when_content_type_starts_with_charset(self, session_mock):

        data = {
            'key': 'value'
        }

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=json.dumps(data),
            headers={
                "Content-Type": "charset=utf-8;application/json"
            }
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.client._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_receive_no_content_response_when_status_code_204_and_content_type_is_not_set(self, session_mock):

        data = {}

        session_mock.return_value = mock.MagicMock(
            status_code=204,
            content=json.dumps(data),
            headers={}
        )

        encoded = json.dumps(data)
        if hasattr(encoded, 'decode'):  # Python 2
            encoded = encoded.decode('utf-8')

        self.assertEqual(
            self.client._makeRequest(),
            json.loads(encoded)
        )

    @mock.patch('requests.Session.request')
    def test_receive_json_error_response_when_content_type_is_not_valid(self, session_mock):

        data = {
            'key': 'value'
        }

        session_mock.return_value = mock.MagicMock(
            status_code=200,
            content=json.dumps(data),
            headers={
                "Content-Type": "wrongContentType"
            }
        )

        with self.assertRaises(HyperwalletAPIException) as exc:
            self.client._makeRequest()

        self.assertEqual(
            exc.exception.message,
            'Invalid Content-Type specified in Response Header'
        )


if __name__ == '__main__':
    unittest.main()
