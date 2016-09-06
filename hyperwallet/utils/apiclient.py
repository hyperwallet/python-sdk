#!/usr/bin/env python

from hyperwallet import __version__


class ApiClient(object):
    """
    The Hyperwallet API Client.

    :param username: The username of this API user.
    :param password: The password of this API user.
    :param server: The target URL to submit HTTP requests.
    """

    def __init__(self, username, password, server):
        """
        Create an instance of the API client.
        This client is used to make the calls to the Hyperwallet API.
        """

        self.username = username
        self.password = password
        self.server = server
        self.version = __version__
