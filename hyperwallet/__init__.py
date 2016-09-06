#!/usr/bin/env python

__author__       = 'The Hyperwallet Developers'
__copyright__    = 'Copyright (c) 2016 Hyperwallet'
__license__      = 'MIT'
__version__      = '0.1.0'
__url__          = 'https://github.com/hyperwallet/python-sdk'
__description__  = 'A Python wrapper around the Hyperwallet API'

# Sane defaults for accessing the Hyperwallet API
SERVER = "https://sandbox.hyperwallet.com"


from .api import Client
