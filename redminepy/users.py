# -*- coding: utf-8 -*-

"""
redminepy.users
~~~~~~~~~~~~~~~

Part of redminepy: Python Redmine API

:copyright: (c) 2012 Rafael Römhild
:license: MIT, see LICENSE for more details.
"""

from redminepy import redmine


class RedmineUserError(Exception):
    """Exception for Redmine API errors"""


class RedmineUserObject(redmine.RedmineApiObject):
    def __init__(self, user, new=False):
        if new:
            user = {u'user': user}
        if not user.has_key('user'):
            raise RedmineUserError('No user in result.')
        redmine.RedmineApiObject.__init__(self, user)

    def __getattr__(self, key):
        return self.__dict__['user'][key]

    def __setattr__(self, key, val):
        if key == '__dict__':
            dict.__setattr__(self, key, val)
        elif self.__dict__.has_key('user'):
            dict.__setitem__(self.user, key, val)


class RedmineUserListObject(redmine.RedmineApiListObject):
    def __init__(self, ulist, resource='users'):
        if not ulist.has_key(resource):
            raise RedmineUserError('No user list in result.')
        redmine.RedmineApiListObject.__init__(self, ulist, resource)

    def get_by_mail(self, mail):
        try:
            if not isinstance(mail, str):
                mail = str(mail)
            user = self.find('mail', mail)[0]
            return RedmineUserObject(user, True)
        except ValueError:
            return None
        except KeyError:
            return None

    def get_by_id(self, uid):
        try:
            if not isinstance(uid, int):
                userid = int(uid)
            user = self.find('id', uid)[0]
            return RedmineUserObject(user, True)
        except ValueError:
            return None
        except KeyError:
            return None

    def get_by_login(self, login):
        try:
            if not isinstance(login, str):
                login = str(login)
            user = self.find('login', login)[0]
            return RedmineUserObject(user, True)
        except ValueError:
            return None
        except KeyError:
            return None
        except IndexError:
            raise RedmineUserError('User not found')


class User(redmine.Redmine):
    """
    Redmine REST Api User Class

    :params host: Hostname for the Redmine instance
    :params apikey: Redmine API-Key
    :params ssl: Whether use https or not
    """

    def __init__(self, host, apikey, ssl= True):
        redmine.Redmine.__init__(self, host, apikey, ssl)
        self._resource = 'users'

    def get(self, uid, include=False):
        params = {}
        page = '%s/%s' % (self._resource, uid)
        if isinstance(include, list):
            include = ','.join(include)
            params = {'include': include}
        return RedmineUserObject(self._get(page, params))

    def list(self, include=None):
        return RedmineUserListObject(self._list())

    def current(self):
        page = '%s/current' % self._resource
        return RedmineUserObject(self._get(page))

    def update(self, data):
        if not isinstance(data, RedmineUserObject):
            raise RedmineUserError('Expecting RedmineUserObject as data.')
        page = '%s/%s' % (self._resource, data.id)
        self._put(page, data)

    def new(self, data):
        if not isinstance(data, RedmineUserObject):
            raise RedmineUserError('Expecting RedmineUserObject as data.')
        self._post(self._resource, data)

    def delete(self, uid):
        page = '%s/%s' % (self._resource, uid)
        self._delete(page)

