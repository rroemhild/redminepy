# -*- coding: utf-8 -*-

"""
redminepy.groups
~~~~~~~~~~~~~~~~

Part of redminepy: Python Redmine API

:copyright: (c) 2012 Rafael Römhild
:license: MIT, see LICENSE for more details.
"""

from redminepy import redmine


class RedmineGroupObject(redmine.RedmineApiObject):
    def __init__(self, group):
        try:
            if group.has_key('group'):
                redmine.RedmineApiObject.__init__(self, group.get('group'))
            else:
                redmine.RedmineApiObject.__init__(self, group)
        except TypeError:
            raise redmine.RedmineApiError('No group in result.')

    def payload(self):
        return {'group': self.__dict__}


class Group(redmine.Redmine):
    """
    Redmine Group Class
    """

    def __init__(self, host, apikey):
        redmine.Redmine.__init__(self, host, apikey)
        self._page = 'groups'

    def get(self, gid, include=False):
        page = '%s/%s' % (self._page, gid)
        if isinstance(include, list):
            include = ','.join(include)
            return RedmineGroupObject(self._get(page, include))
        return RedmineGroupObject(self._get(page))

    def list(self):
        return self._get(self._page)

    def update(self, gid, data):
        page = '%s/%s' % (self._page, gid)
        self._put(page, data.payload())

    def new(self, data):
        self._post(self._page, data.payload())

    def delete(self, gid):
        page = '%s/%s' % (self._page, id)
        self._delete(page)

    def add(self, gid, uid):
        """
        Add a user to a group

        :param gid: Group ID
        :param uid: User ID
        """

        data = {'user_id': str(uid)}
        page = '%s/%s/users' % (self._page, gid)
        self._post(page, data)

    def rem(self, gid, uid):
        """
        Remove a user from a group

        :param gid: Group ID
        :param uid: User ID
        """

        page = '%s/%s/users/%s' % (self._page, gid, uid)
        self._delete(page)

