# -*- coding: utf-8 -*-

"""
redminepy.groups
~~~~~~~~~~~~~~~~

Part of redminepy: Python Redmine API

:copyright: (c) 2012 Rafael Römhild
:license: MIT, see LICENSE for more details.
"""

from redminepy import redmine


class RedmineGroupError(Exception):
    """Exception for Redmine API errors"""


class RedmineGroupObject(redmine.RedmineApiObject):
    def __init__(self, group, new=False):
        if new:
            group = {u'group': group}
        if not group.has_key('group'):
            raise RedmineGroupError('No group in result.')
        redmine.RedmineApiObject.__init__(self, group)

    def __getattr__(self, key):
        return self.__dict__['group'][key]

    def __setattr__(self, key, val):
        if key == '__dict__':
            dict.__setattr__(self, key, val)
        elif self.__dict__.has_key('group'):
            dict.__setitem__(self.user, key, val)


class RedmineGroupListObject(redmine.RedmineApiListObject):
    def __init__(self, glist, resource='groups'):
        if not glist.has_key(resource):
            raise RedmineGroupError('No group list in result.')
        redmine.RedmineApiListObject.__init__(self, glist, resource)

    def get_by_name(self, name):
        try:
            if not isinstance(name, str):
                name = str(name)
            group = self.find('name', name)[0]
            return RedmineGroupObject(group, True)
        except ValueError:
            return None
        except KeyError:
            return None

    def get_by_id(self, gid):
        try:
            if not isinstance(gid, int):
                gid = int(gid)
            group = self.find('id', gid)[0]
            return RedmineGroupObject(group, True)
        except ValueError:
            return None
        except KeyError:
            return None


class Group(redmine.Redmine):
    """
    Redmine REST API Group Class

    :params host: Hostname for the Redmine instance
    :params apikey: Redmine API-Key
    :params ssl: Whether use https or not
    """

    def __init__(self, host, apikey, ssl=True):
        redmine.Redmine.__init__(self, host, apikey, ssl)
        self._resource = 'groups'

    def get(self, gid, include=False):
        params = {}
        page = '%s/%s' % (self._resource, gid)
        if isinstance(include, list):
            include = ','.join(include)
            params = {'include': include}
        return RedmineGroupObject(self._get(page, params))

    def list(self, include=None):
        return RedmineGroupListObject(self._list())

    def update(self, gid, data):
        if not isinstance(data, RedmineGroupObject):
            raise RedmineGroupError('Expecting RedmineGroupObject as data.')
        page = '%s/%s' % (self._resource, gid)
        self._put(page, data)

    def new(self, data):
        if not isinstance(data, RedmineGroupObject):
            raise RedmineGroupError('Expecting RedmineGroupObject as data.')
        self._post(self._resource, data)

    def delete(self, gid):
        page = '%s/%s' % (self._resource, gid)
        self._delete(page)

    def add(self, gid, uid):
        """
        Add a user to a group

        :param gid: Group ID
        :param uid: User ID
        """

        data = {'user_id': uid}
        page = '%s/%s/users' % (self._resource, gid)
        self._post(page, data)

    def rem(self, gid, uid):
        """
        Remove a user from a group

        :param gid: Group ID
        :param uid: User ID
        """

        page = '%s/%s/users/%s' % (self._resource, gid, uid)
        self._delete(page)

