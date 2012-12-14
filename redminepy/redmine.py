# -*- coding: utf-8 -*-

"""
redminepy.redmine
~~~~~~~~~~~~~~~~~

Part of redminepy: Python Redmine API

:copyright: (c) 2012 Rafael Römhild
:license: MIT, see LICENSE for more details.
"""

import logging
import requests

try:
    import json
except ImportError:
    import simplejson as json


class RedmineApiError(Exception):
    """Exception for Redmine API errors"""


class RedmineApiObject(object):
    def __init__(self, d):
        self.__dict__ = d

    def __str__(self):
        return str(self.__dict__)


class Redmine(object):
    """
    Python Redmine Project API Class
    """

    def __init__(self, host, apikey, ssl=True):
        self._host = host
        self._key = apikey
        self._scheme = 'https'
        self._headers = {'Content-Type': 'application/json'}

        if not ssl:
            self._scheme = 'http'

    def _get(self, page, include=None):
        url = '%s://%s/%s.json?key=%s' % (self._scheme, self._host,
                                          page, self._key)
        if include:
            url = '%s&include=%s' % (url, include)
        r = requests.get(url, headers=self._headers)
        return r.json

    def _post(self, page, payload):
        url = '%s://%s/%s.json?key=%s' % (self._scheme, self._host,
                                          page, self._key)
        payload = json.dumps(payload)
        r = requests.post(url, data=payload, headers=self._headers)
        if not r.status_code == requests.codes.created and not \
          r.status_code == requests.codes.ok:
            raise RedmineApiError(r.text)

    def _put(self, page, payload):
        url = '%s://%s/%s.json?key=%s' % (self._scheme, self._host,
                                          page, self._key)
        payload = json.dumps(payload)
        r = requests.put(url, data=payload, headers=self._headers)
        if not r.status_code == requests.codes.ok:
            raise RedmineApiError(r.text)

    def _delete(self, page):
        url = '%s://%s/%s.json?key=%s' % (self._scheme, self._host,
                                          page, self._key)
        r = requests.delete(url, headers=self._headers)
        if not r.status_code == requests.codes.ok:
            raise RedmineApiError(r.text)

