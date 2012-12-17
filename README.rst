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

    data = {'login': 'newuser',
            'firstname': 'New',
            'lastname': 'User',
            'mail': 'newuser@example.tld'
            }
    ruser.new(users.RedmineUserObject(data)

Add user to group
-----------------

Add an existing user to a group::

    from redminepy import groups

    host = 'redmine.example.tld'
    apikey = 'redmineapikey'

    group = groups.Group(host, apikey)
    gid, uid = 453, 390
    group.add(gid, uid)

