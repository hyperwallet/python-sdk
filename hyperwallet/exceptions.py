#!/usr/bin/env python


class HyperwalletException(Exception):
    '''
    An Exception raised when the SDK is used incorrectly.
    '''


class HyperwalletAPIException(Exception):
    '''
    An Exception raised when the API response is an error.
    '''
