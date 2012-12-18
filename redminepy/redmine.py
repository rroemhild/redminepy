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

    def get_json(self):
        return json.dumps(dict(self.__dict__))


class RedmineApiListObject(RedmineApiObject):
    def __init__(self, d, resource=None):
        RedmineApiObject.__init__(self, d)
        self._resource = resource

    def find(self, key, val=None):
        entry_list = []
        for entry in self.__getattribute__(self._resource):
            if entry.has_key(key):
                if val:
                    if val in entry[key]:
                        entry_list.append(entry)
                else:
                    entry_list.append(entry)
        return entry_list


class Redmine(object):
    """
    Main Class for the Redmine Project REST API.

    :params host: Hostname for the Redmine instance
    :params apikey: Redmine API-Key
    :params ssl: Whether use https or not
    """

    def __init__(self, host, apikey, ssl=True):
        self._host = host
        self._scheme = 'https'
        self._headers = {'Content-Type': 'application/json',
                         'X-Redmine-API-Key': apikey}

        if not ssl:
            self._scheme = 'http'

    def _get(self, page, params={}):
        url = '%s://%s/%s.json' % (self._scheme, self._host, page)
        if not isinstance(params, dict):
            raise RedmineApiError('params must be a dict.')
        r = requests.get(url, headers=self._headers, params=params)
        return r.json

    def _post(self, page, data={}):
        url = '%s://%s/%s.json' % (self._scheme, self._host, page)
        r = requests.post(url, data=data.get_json(), headers=self._headers)
        if not r.status_code == requests.codes.created and not \
          r.status_code == requests.codes.ok:
            raise RedmineApiError(r.text)

    def _put(self, page, data={}):
        url = '%s://%s/%s.json' % (self._scheme, self._host, page)
        r = requests.put(url, data=data.get_json(), headers=self._headers)
        if not r.status_code == requests.codes.ok:
            raise RedmineApiError(r.text)

    def _delete(self, page):
        url = '%s://%s/%s.json' % (self._scheme, self._host, page)
        r = requests.delete(url, headers=self._headers)
        if not r.status_code == requests.codes.ok:
            raise RedmineApiError(r.text)

    def _list(self):
        offset = 0
        limit = 100
        params = {'offset': offset, 'limit': limit}
        result = self._get(self._resource, params)
        total = result.get('total_count')
        if total > params['limit']:
            getrange = total / params['limit']
            for request in range(0, getrange):
                params['offset'] = params['offset'] + limit
                params['limit'] = params['limit'] + limit
                next = self._get(self._resource, params).get(self._resource)
                for entry in next:
                    result.get(self._resource).append(entry)
        return result

