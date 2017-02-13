#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, send_file, g, session
from os.path import dirname, abspath

STATIC_PATH = abspath(dirname(abspath(__file__)) + '/../static/')

app = Flask(__name__, static_folder=STATIC_PATH)
app.config.from_object('config.MainConfig')


@app.route('/')
def index():
    data = dict()
    data['current_page'] = 'index'
    data['info'] = {"pages": 0, "items": []}

    return render_template('index.html', **data)

