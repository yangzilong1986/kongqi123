#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, abspath
from flask import Flask


def create_app(config=None):
    STATIC_PATH = abspath(dirname(abspath(__file__)) + '/../static/')
    app = Flask(__name__, static_folder=STATIC_PATH)
    if config is not None:
        app.config.from_pyfile(config)
    else:
        app.config.from_object('config.MainConfig')
    return app

