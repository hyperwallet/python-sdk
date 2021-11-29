.. image:: https://travis-ci.org/hyperwallet/python-sdk.svg?branch=master
  :target: https://travis-ci.org/hyperwallet/python-sdk/builds
.. image:: https://coveralls.io/repos/github/hyperwallet/python-sdk/badge.svg?branch=master
  :target: https://coveralls.io/github/hyperwallet/python-sdk?branch=master

===========================
Hyperwallet REST SDK (Beta)
===========================

A library to manage users, transfer methods and payments through the Hyperwallet Rest V3 API

Prerequisites
-------------

Hyperwallet's Python server SDK requires at minimum Python 3.5 and above.

Installation
------------

.. code::

    $ pip install hyperwallet-sdk

Documentation
-------------

Documentation is available at http://hyperwallet.github.io/python-sdk

API Overview
------------

To write an app using the SDK

* Register for a sandbox account and get your username, password and program
  token at the `Hyperwallet Program Portal <https://portal.hyperwallet.com>`_.
* Import the Hyperwallet module

.. code::

    import hyperwallet

* Create an instance of the Hyperwallet Client (with username, password and
  program token)

.. code::

    api = hyperwallet.Api(
        "test-user",
        "test-pass",
        "prg-12345"
    )

* Start making API calls (e.g. create a user)

.. code::

    data = {
        clientUserId: "test-client-id-1",
        profileType: "INDIVIDUAL",
        firstName: "Daffy",
        lastName: "Duck",
        email: "testmail-1@hyperwallet.com",
        addressLine1: "123 Main Street",
        city: "Austin",
        stateProvince: "TX",
        country: "US",
        postalCode: "78701",
        programToken: "[PROGRAM TOKEN]"
    }

    response = api.createUser(data)

Development
-----------

Set up a virtual environment:

.. code::

    $ virtualenv venv
    $ source venv/bin/activate

Install development dependencies:

.. code::

    $ make dev

Run the tests:

.. code::

    $ make test

Compile the documentation:

.. code::

    $ make docs

Requirements
------------

The Hyperwallet API uses TLS 1.2. Please ensure that your SSL library
supports TLS 1.2.

Reference
---------

`REST API Reference <https://portal.hyperwallet.com/docs>`_

License
-------

`MIT <https://raw.githubusercontent.com/hyperwallet/python-sdk/master/LICENSE>`_
