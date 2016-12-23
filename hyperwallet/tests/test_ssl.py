#!/usr/bin/env python

import unittest
import hyperwallet

from hyperwallet.config import SERVER
from hyperwallet.exceptions import HyperwalletException


class ApiClientInitializationTest(unittest.TestCase):

    def test_incompatible_ssl(self):

        import ssl
        del ssl.PROTOCOL_TLSv1_2

        self.assertRaises(
            HyperwalletException,
            hyperwallet.utils.ApiClient,
            'test-user',
            'test-pass',
            SERVER
        )
