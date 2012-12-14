# -*- coding: utf-8 -*-

"""
redminepy.users
~~~~~~~~~~~~~~~

Part of redminepy: Python Redmine API

:copyright: (c) 2012 Rafael Römhild
:license: MIT, see LICENSE for more details.
"""

from redminepy import redmine


class RedmineUserObject(redmine.RedmineApiObject):
    def __init__(self, user):
        try:
            if user.has_key('user'):
                redmine.RedmineApiObject.__init__(self, user.get('user'))
            else:
                redmine.RedmineApiObject.__init__(self, user)
        except TypeError:
            raise redmine.RedmineApiError('No user in result.')

    def payload(self):
        return {'user': self.__dict__}


class User(redmine.Redmine):
    """
    Redmine User Class
    """

    def __init__(self, host, apikey):
        redmine.Redmine.__init__(self, host, apikey)
        self._page = 'users'

    def get(self, uid, include=False):
        page = '%s/%s' % (self._page, uid)
        if isinstance(include, list):
            include = ','.join(include)
            return RedmineUserObject(self._get(page, include))
        return RedmineUserObject(self._get(page))

    def list(self):
        return self._get(self._page)

    def current(self):
        page = 'users/current'
        return RedmineUserObject(self._get(page))

    def update(self, uid, data):
        page = '%s/%s' % (self._page, uid)
        self._put(page, data.payload())

    def new(self, data):
        self._post(self._page, data.payload())

    def delete(self, uid):
        page = '%s/%s' % (self._page, uid)
        self._delete(page)

