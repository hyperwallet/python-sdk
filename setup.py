#!/usr/bin/env python

import os
import re
import codecs

from setuptools import setup, find_packages


ground = os.path.abspath(os.path.dirname(__file__))

def read(filename):
    with codecs.open(os.path.join(ground, filename), 'rb', 'utf-8') as file:
        return file.read()

metadata = read(os.path.join(ground, 'hyperwallet', '__init__.py'))

def extract_metaitem(meta):
    meta_match = re.search(r"""^__{meta}__\s+=\s+['\"]([^'\"]*)['\"]""".format(meta=meta), metadata, re.MULTILINE)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError('Unable to find __{meta}__ string.'.format(meta=meta))

setup(
    name = 'hyperwallet-sdk',
    url = extract_metaitem('url'),
    author = extract_metaitem('author'),
    author_email = extract_metaitem('email'),
    version = extract_metaitem('version'),
    license = extract_metaitem('license'),
    description = extract_metaitem('description'),
    long_description = (read('README.rst') + '\n\n' +
                        read('CHANGELOG.rst')),
    maintainer = extract_metaitem('author'),
    maintainer_email = extract_metaitem('email'),
    packages = find_packages(exclude = ('tests', 'doc')),
    install_requires = ['requests', 'requests-toolbelt', 'jwcrypto', 'python-jose'],
    test_suite = 'nose.collector',
    tests_require = [ 'mock', 'nose'],
    keywords='hyperwallet api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
