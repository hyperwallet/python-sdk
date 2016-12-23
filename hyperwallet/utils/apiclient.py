#!/usr/bin/env python

import sys
import ssl
import json
import urlparse
import requests

from hyperwallet.exceptions import HyperwalletException
from requests_toolbelt.adapters.ssl import SSLAdapter
from hyperwallet import __version__


class ApiClient(object):
    '''
    The Hyperwallet API Client.

    :param username: The username of this API user. **REQUIRED**
    :param password: The password of this API user. **REQUIRED**
    :param server: The base URL of the API. **REQUIRED**
    '''

    def __init__(self, username, password, server):
        '''
        Create an instance of the API client.
        This client is used to make the calls to the Hyperwallet API.
        '''

        if not hasattr(ssl, 'PROTOCOL_TLSv1_2'):
            raise HyperwalletException(
                'Please update your SSL library to one with TLS 1.2 support.'
            )

        # Base headers and the custom User-Agent to identify this client as the
        # Hyperwallet SDK.
        self.baseHeaders = {
            'User-Agent': 'Hyperwallet Python SDK v{}'.format(__version__),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self.username = username
        self.password = password
        self.server = server

        # The complete base URL of the API.
        self.baseUrl = urlparse.urljoin(self.server, '/rest/v3/')

        # The default connection to persist authentication and SSL settings.
        defaultSession = requests.Session()
        defaultSession.mount(self.server, SSLAdapter(ssl.PROTOCOL_TLSv1_2))
        defaultSession.auth = (self.username, self.password)
        defaultSession.headers = self.baseHeaders

        self.session = defaultSession

    def _makeRequest(self,
                     method=None,
                     url=None,
                     data=None,
                     headers=None,
                     params=None):
        '''
        Process an API response to ensure a JSON object is returned always.

        :param method: The HTTP method to use for the request. **REQUIRED**
        :param url: A partial URL to specify the API endpoint. **REQUIRED**
        :param data: A dictionary containing data for the request body.
        :param headers: A dictionary containing additional request headers.
        :param params: A dictionary containing query parameters.
        :returns:
            A JSON object containing the response data or an error object.

        .. note::
            The Hyperwallet API supports **GET**, **POST**, and **PUT**.
        '''

        body = {
            'errors': [
                {
                    'message': 'Could not communicate with {}'.format(
                        self.server
                    ),
                    'code': 'COMMUNICATION_ERROR'
                }
            ]
        }

        try:
            response = self.session.request(method=method,
                                            url=urlparse.urljoin(
                                                self.baseUrl, url
                                            ),
                                            data=data,
                                            headers=headers,
                                            params=params
                                            )
        except:
            return body

        if response.ok:
            body = response.json()
        else:
            if (not response.ok and
                    response.content and
                    response.json().get('errors')):

                # Overwrite the general error response if errors were returned
                body['errors'] = response.json().get('errors')

        return body

    def doGet(self, partialUrl, params={}):
        '''
        Submit a GET to the API.

        :param partialUrl:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param params: A dictionary containing query parameters.
        :returns: The API response.
        '''

        return self._makeRequest(method='GET',
                                 url=partialUrl,
                                 params=params
                                 )

    def doPost(self, partialUrl, data, headers={}):
        '''
        Submit a POST to the API.

        :param partialUrl:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param data:
            A dictionary containing data for the request body. **REQUIRED**
        :param headers: A dictionary containing additional request headers.
        :returns: The API response.
        '''

        return self._makeRequest(method='POST',
                                 url=partialUrl,
                                 data=json.dumps(data).encode('utf-8'),
                                 headers=headers
                                 )

    def doPut(self, partialUrl, data):
        '''
        Submit a PUT to the API.

        :param partialUrl:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param data:
            A dictionary containing data for the request body. **REQUIRED**
        :returns: The API response.
        '''

        return self._makeRequest(method='PUT',
                                 url=partialUrl,
                                 data=json.dumps(data).encode('utf-8')
                                 )
