# coding:utf-8

import json
from flask import Flask, render_template, request, redirect, url_for, send_file, g, session
from os.path import dirname, abspath
from core.history import History
from core.weather import Weather
from core.yahoo import Yahoo

STATIC_PATH = abspath(dirname(abspath(__file__)) + '/../static/')

app = Flask(__name__, static_folder=STATIC_PATH)
app.config.from_object('config.MainConfig')


@app.route('/')
def index():
    yahoo_client = Yahoo.factory()
    woeid = yahoo_client.get_woeid_by_name(u'上海')
    if not woeid:
        return u'不支持的城市名'
    print 'woeid: ', woeid

    weather_info = yahoo_client.get_weather(woeid)
    print weather_info

    data = dict()
    data['req_args'] = dict(request.args.items())

    return render_template('index.html', **data)


@app.route('/city')
def city_index():
    weather_client = Weather.factory()
    cities = weather_client.get_group_weather_city()

    data = dict()
    data['req_args'] = dict(request.args.items())
    data['cities'] = cities

    return render_template('city.html', **data)


@app.route('/data')
def data_index():
    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': u'上海',
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('data_index.html', **data)

