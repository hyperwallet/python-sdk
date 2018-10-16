#!/usr/bin/env python

import unittest
import time
import json
import os.path

from jwcrypto import jwk, jws as cryptoJWS
from jwcrypto.common import json_encode
from hyperwallet.exceptions import HyperwalletException
from hyperwallet.utils.encryption import Encryption
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class EncryptionTest(unittest.TestCase):

    def test_should_successfully_encrypt_and_decrypt_text_message(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        testMessage = 'Message for test'
        encryptedMessage = encryption.encrypt(testMessage)
        decryptedMessage = encryption.decrypt(encryptedMessage)
        self.assertEqual(decryptedMessage, testMessage)

    def test_should_fail_decryption_when_wrong_private_key_is_used(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath1 = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath1 = os.path.join(localDir, 'resources', 'public-jwkset1')
        clientPath2 = os.path.join(localDir, 'resources', 'private-jwkset2')
        hyperwalletPath2 = os.path.join(localDir, 'resources', 'public-jwkset2')
        encryption1 = Encryption(clientPath1, hyperwalletPath1)
        encryption2 = Encryption(clientPath2, hyperwalletPath2)
        testMessage = 'Message for test'
        encryptedMessage = encryption1.encrypt(testMessage)

        with self.assertRaises(HyperwalletException) as exc:
            encryption2.decrypt(encryptedMessage)

        self.assertEqual(exc.exception.message, 'No recipient matched the provided key["Failed: [ValueError(\'Decryption failed.\',)]"]')

    def test_should_fail_signature_verification_when_wrong_public_key_is_used(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath1 = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath1 = os.path.join(localDir, 'resources', 'public-jwkset1')
        clientPath2 = os.path.join(localDir, 'resources', 'private-jwkset2')
        hyperwalletPath2 = os.path.join(localDir, 'resources', 'public-jwkset2')
        encryption1 = Encryption(clientPath1, hyperwalletPath1)
        encryption2 = Encryption(clientPath1, hyperwalletPath2)
        testMessage = 'Message for test'
        encryptedMessage = encryption1.encrypt(testMessage)

        with self.assertRaises(HyperwalletException) as exc:
            encryption2.decrypt(encryptedMessage)

        self.assertEqual(exc.exception.message, 'Signature verification failed.')

    def test_should_throw_exception_when_wrong_jwk_key_set_location_is_given(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = 'wrong_keyset_path'
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath)
        testMessage = 'Message for test'

        with self.assertRaises(HyperwalletException) as exc:
            encryptedMessage = encryption.encrypt(testMessage)

        self.assertEqual(exc.exception.message, 'Wrong JWK key set location path = wrong_keyset_path')

    def test_should_throw_exception_when_not_supported_encryption_algorithm_is_given(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = os.path.join(localDir, 'resources', 'public-jwkset1')
        encryption = Encryption(clientPath, hyperwalletPath, 'unsupported_encryption_algorithm')
        testMessage = 'Message for test'

        with self.assertRaises(HyperwalletException) as exc:
            encryptedMessage = encryption.encrypt(testMessage)

        self.assertEqual(exc.exception.message, 'JWK set doesn\'t contain key with algorithm = unsupported_encryption_algorithm')

    def test_should_throw_exception_when_jws_signature_does_not_contain_exp_header_param(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = '/public-jwkset1'
        encryption = Encryption(clientPath, hyperwalletPath)

        jwsKeySet = self.__getJwkKeySet(location=clientPath)
        jwkSignKey = self.__findJwkKeyByAlgorithm(jwkKeySet=jwsKeySet, algorithm='RS256')
        privateKeyToSign = jwk.JWK(**jwkSignKey)
        body = "Test message"
        jwsToken = cryptoJWS.JWS(body.encode('utf-8'))
        jwsToken.add_signature(privateKeyToSign, None, json_encode({
            "alg": "RS256",
            "kid": jwkSignKey['kid']
        }))
        signedBody = jwsToken.serialize(True)

        with self.assertRaises(HyperwalletException) as exc:
            encryption.checkJwsExpiration(signedBody)

        self.assertEqual(exc.exception.message, 'While trying to verify JWS signature no [exp] header is found')

    def test_should_throw_exception_when_jws_signature_exp_header_param_is_not_integer(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = '/public-jwkset1'
        encryption = Encryption(clientPath, hyperwalletPath)

        jwsKeySet = self.__getJwkKeySet(location=clientPath)
        jwkSignKey = self.__findJwkKeyByAlgorithm(jwkKeySet=jwsKeySet, algorithm='RS256')
        privateKeyToSign = jwk.JWK(**jwkSignKey)
        body = "Test message"
        jwsToken = cryptoJWS.JWS(body.encode('utf-8'))
        jwsToken.add_signature(privateKeyToSign, None, json_encode({
            "alg": "RS256",
            "exp": "153356exp",
            "kid": jwkSignKey['kid']
        }))
        signedBody = jwsToken.serialize(True)

        with self.assertRaises(HyperwalletException) as exc:
            encryption.checkJwsExpiration(signedBody)

        self.assertEqual(exc.exception.message, 'Wrong value in [exp] header of JWS signature, must be integer')

    def test_should_throw_exception_when_jws_signature_has_expired(self):

        localDir = os.path.abspath(os.path.dirname(__file__))
        clientPath = os.path.join(localDir, 'resources', 'private-jwkset1')
        hyperwalletPath = '/public-jwkset1'
        encryption = Encryption(clientPath, hyperwalletPath)

        jwsKeySet = self.__getJwkKeySet(location=clientPath)
        jwkSignKey = self.__findJwkKeyByAlgorithm(jwkKeySet=jwsKeySet, algorithm='RS256')
        privateKeyToSign = jwk.JWK(**jwkSignKey)
        body = "Test message"
        jwsToken = cryptoJWS.JWS(body.encode('utf-8'))
        jwsToken.add_signature(privateKeyToSign, None, json_encode({
            "alg": "RS256",
            "exp": int(time.time()) - 6000,
            "kid": jwkSignKey['kid']
        }))
        signedBody = jwsToken.serialize(True)

        with self.assertRaises(HyperwalletException) as exc:
            encryption.checkJwsExpiration(signedBody)

        self.assertEqual(exc.exception.message, 'JWS signature has expired, checked by [exp] JWS header')

    def __getJwkKeySet(self, location):

        try:
            URLValidator()(location)
        except ValidationError:
            if os.path.isfile(location):
                with open(location) as f:
                    return f.read()
            else:
                raise HyperwalletException('Wrong JWK key set location path = ' + location)

        return requests.get(location).text

    def __findJwkKeyByAlgorithm(self, jwkKeySet, algorithm):

        try:
            keySet = json.loads(jwkKeySet)
        except ValueError:
            raise HyperwalletException('Wrong JWK key set' + jwkKeySet)

        for key in keySet['keys']:
            if key['alg'] == algorithm:
                return key

        raise HyperwalletException('JWK set doesn\'t contain key with algorithm = ' + algorithm)


if __name__ == '__main__':
    unittest.main()
