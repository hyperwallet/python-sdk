#!/usr/bin/env python

from hyperwallet import SERVER
from utils import ApiClient


class Client(object):
    """
    A Python interface for the Hyperwallet API.

    :param username: The username of this API user.
    :param password: The password of this API user.
    :param programToken: The token for the program this user is accessing.
    :param server:
        Defaults to our sandbox URL
        Users will pass in their UAT or Production URL when available.
    """

    def __init__(self, username, password, programToken, server = SERVER):
        """
        Create an instance of the Client interface.
        This is the main interface the user will call to interact with the API.
        """

        self.username = username
        self.password = password
        self.programToken = programToken
        self.server = server

        self.apiClient = ApiClient(self.username, self.password, self.server)
