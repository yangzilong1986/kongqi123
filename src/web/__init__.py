#!/usr/bin/env python
# encoding: utf-8

import json
import base64
import re
from os.path import dirname, abspath
from flask import Flask


def create_app(config=None):
    STATIC_PATH = abspath(dirname(abspath(__file__)) + '/static/')
    app = Flask(__name__, static_folder=STATIC_PATH)
    if config is not None:
        app.config.from_pyfile(config)
    else:
        app.config.from_object('config.MainConfig')
    return app


class LoginUser(object):

    def __init__(self, _id):
        if isinstance(_id, str) or isinstance(_id, unicode):
            _id = json.loads(base64.urlsafe_b64decode(str(_id)))
        self._id = _id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return base64.urlsafe_b64encode(json.dumps(self._id))

    @property
    def name(self):
        return self._id['name']

    @property
    def user_id(self):
        return self._id['uid']

    @property
    def openid(self):
        return self._id['openid']


