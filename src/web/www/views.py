#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, send_file, g, session
from os.path import dirname, abspath
from core.history import History

STATIC_PATH = abspath(dirname(abspath(__file__)) + '/../static/')

app = Flask(__name__, static_folder=STATIC_PATH)
app.config.from_object('config.MainConfig')


@app.route('/')
def index():
    date_start = request.args.get('sales_start', default='')
    date_end = request.args.get('sales_end', default='')

    condition = {

    }
    other = {
        'city_name': u'上海',
    }
    page = request.args.get('page', 1, type=int)
    product_client = ProductApiClient.factory()
    info = product_client.search(condition, page, 20, other)

    data = dict()
    data['info'] = {"pages": 0, "items": []}

    return render_template('index.html', **data)

