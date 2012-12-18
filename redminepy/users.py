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
    def __init__(self, user,  new=False):
        if new:
            user = {'user': user}
        if not user.has_key('user'):
            raise redmine.RedmineApiError('No user in result.')
        redmine.RedmineApiObject.__init__(self, user)

    def __getattr__(self, key):
        return self.get(key)
        
    def get(self, key):
        user = dict(self.user)
        return user[key]


class RedmineUserListObject(redmine.RedmineApiListObject):
    def __init__(self, ulist):
        if not ulist.has_key('users'):
            raise redmine.RedmineApiError('No user list in result.')
        redmine.RedmineApiListObject.__init__(self, ulist)

    def search(self, key, val=None):
        user_list = []
        for user in self.__getattribute__('users'):
            if user.has_key(key):
                if val:
                    if user[key] == val:
                        user_list.append(user)
                else:
                    user_list.append(user)
        return user_list

    def get_by_mail(self, mail):
        try:
            if not isinstance(mail, str):
                mail = int(mail)
            user = self.search('mail', mail)[0]
            return RedmineUserObject(user, True)
        except ValueError:
            return None
        except KeyError:
            return None

    def get_by_id(self, userid):
        try:
            if not isinstance(userid, int):
                userid = int(userid)
            user = self.search('id', userid)[0]
            return RedmineUserObject(user, True)
        except ValueError:
            return None
        except KeyError:
            return None

    def get_by_login(self, login):
        try:
            if not isinstance(login, str):
                login = int(login)
            user = self.search('login', login)[0]
            return RedmineUserObject(user, True)
        except ValueError:
            return None
        except KeyError:
            return None
        except IndexError:
            raise redmine.RedmineApiError('User not found')


class User(redmine.Redmine):
    """
    Redmine User Class
    """

    def __init__(self, host, apikey):
        redmine.Redmine.__init__(self, host, apikey)
        self._page = 'users'

    def get(self, uid, include=[]):
        payload = {}
        page = '%s/%s' % (self._page, uid)
        if isinstance(include, list):
            include = ','.join(include)
            payload = {'include': include}
        return RedmineUserObject(self._get(page, payload))

    def list(self):
        offset = 0
        limit = 100
        payload = {'offset': offset, 'limit': limit}
        result = self._get(self._page, payload)
        total = result.get('total_count')
        if total > payload['limit']:
            getrange = total / payload['limit']
            for request in range(0, getrange):
                payload['offset'] = payload['offset'] + limit
                payload['limit'] = payload['limit'] + limit
                next_users = self._get(self._page, payload).get('users')
                for user in next_users:
                    result.get('users').append(user)
        return RedmineUserListObject(result)

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

