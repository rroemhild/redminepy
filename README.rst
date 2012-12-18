Redminepy
#########

Redminepy is a Python module to access the `Redmine <http://www.redmine.org/>`_
`Rest API <http://www.redmine.org/projects/redmine/wiki/Rest_api>`_.

At this time ``redminepy`` only can talk to the
`Rest Users <http://www.redmine.org/projects/redmine/wiki/Rest_Users>`_
and the
`Rest Groups <http://www.redmine.org/projects/redmine/wiki/Rest_Groups>`_
API and should be considerd as experimental.


Requirements
============

- Redmine 1.1.0
- python 2.6 or newer
- requests


Install
=======

Get the latest version from Github::

    pip install -e git://github.com/rroemhild/redminepy.git#egg=redminepy


Example
=======

Get user
--------

Get user information::

    from redminepy import users

    host = 'redmine.example.tld'
    apikey = 'redmineapikey'

    ruser = users.User(host, apikey)
    user = ruser.get(3)

    print user
    print user.login

Create new user
---------------

Create a new user::

    from redminepy import users

    host = 'redmine.example.tld'
    apikey = 'redmineapikey'

    ruser = users.User(host, apikey)

    data = {u'login': u'newuser',
            u'firstname': u'New',
            u'lastname': u'User',
            u'mail': u'newuser@example.tld'
            }
    ruser.new(users.RedmineUserObject(data, True)

Add user to group
-----------------

Add an existing user to a group::

    from redminepy import groups

    host = 'redmine.example.tld'
    apikey = 'redmineapikey'

    group = groups.Group(host, apikey)
    gid, uid = 2, 111
    group.add(gid, uid)

