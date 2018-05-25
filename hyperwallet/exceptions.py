#!/usr/bin/env python


class HyperwalletException(Exception):
    '''
    An Exception raised when the SDK is used incorrectly.
    '''

    @property
    def message(self):
        return self.__dict__.get('message', None) or getattr(self, 'args')[0]


class HyperwalletAPIException(Exception):
    '''
    An Exception raised when the API response is an error.
    '''

    @property
    def message(self):
        return self.__dict__.get('message', None) or getattr(self, 'args')[0]
