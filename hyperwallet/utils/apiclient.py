#!/usr/bin/env python

import ssl
import json
import requests

from requests.auth import HTTPBasicAuth
from requests_toolbelt.adapters.ssl import SSLAdapter


from hyperwallet import __version__


class ApiClient(object):
    """
    The Hyperwallet API Client.

    :param username: The username of this API user.
    :param password: The password of this API user.
    :param server: The target URL to submit HTTP requests.
    """

    """
    The current version of this SDK.
    """
    version = __version__

    """
    The custom User Agent to identify this client as our SDK.
    """
    baseHeaders = {
        "User-Agent": "Hyperwallet Python SDK v{}".format(version),
        "Accept": "application/json"
    }

    def __init__(self, username, password, server):
        """
        Create an instance of the API client.
        This client is used to make the calls to the Hyperwallet API.
        """

        self.username = username
        self.password = password
        self.server = server

    def doPost(self, partialUrl, data, params = {}):
        """
        Submit a POST to the server.
        Returns the response.
        """

        headers = self.baseHeaders
        headers["Content-Type"] = "application/json"

        with requests.Session() as s:
            s.mount(self.server, SSLAdapter(ssl.PROTOCOL_TLSv1_2))

            response = s.post(
                # TODO need to join server safely
                self.server + "/rest/v3/" + partialUrl,
                data = json.dumps(data).encode('utf-8'),
                params = params,
                headers = headers,
                auth = (self.username, self.password)
            )

            return response

    def doPut(self, partialUrl, data, params = {}):
        """
        Submit a PUT to the server.
        Returns the response.
        """

        pass

    def doGet(self, partialUrl, params = {}):
        """
        Submit a GET to the server.
        Returns the response.
        """

        pass
