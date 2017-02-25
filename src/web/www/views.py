# coding:utf-8

import json
from flask import Flask, render_template, request, redirect, url_for, send_file, g, session
from os.path import dirname, abspath
from core.history import History
from core.weather import Weather
from core.yahoo import Yahoo
from core.spider import Spider

STATIC_PATH = abspath(dirname(abspath(__file__)) + '/../static/')

app = Flask(__name__, static_folder=STATIC_PATH)
app.config.from_object('config.MainConfig')


@app.before_request
def before_request():
    if 'city_name' in session:
        g.city_name = session['city_name']


@app.route('/city')
def city_index():
    weather_client = Weather.factory()
    cities = weather_client.get_group_weather_city()

    data = dict()
    data['current_page'] = 'city'
    data['req_args'] = dict(request.args.items())
    data['cities'] = cities

    return render_template('city.html', **data)


@app.route('/')
def index():
    city_name = u'上海'
    yahoo_client = Yahoo.factory()
    woeid = yahoo_client.get_woeid_by_name(city_name)
    if not woeid:
        return u'不支持的城市名'
    print 'woeid: ', woeid

    today_weather = yahoo_client.get_today_weather(woeid)
    print today_weather

    forecast_weather = yahoo_client.get_forecast_weather(woeid)
    print forecast_weather

    data = dict()
    data['current_page'] = 'index'
    data['city_name'] = city_name
    data['today_weather'] = today_weather
    data['forecast_weather'] = forecast_weather
    data['req_args'] = dict(request.args.items())

    return render_template('index.html', **data)


@app.route('/data')
def data_index():
    city_name = u'上海'

    spider_client = Spider.factory()
    job_list = spider_client.list_job()
    print str(job_list)

    data = dict()
    data['current_page'] = 'data'
    data['req_args'] = dict(request.args.items())
    data['job_list'] = job_list

    return render_template('data/index.html', **data)


@app.route('/data/history')
def data_history():
    city_name = u'上海'

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': city_name,
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'data'
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('data/history.html', **data)


@app.route('/data/weather')
def data_weather():
    city_name = u'上海'

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': city_name,
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'data'
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('data/weather.html', **data)


@app.route('/report')
def report_index():
    city_name = u'上海'

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': city_name,
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'report'
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('report/index.html', **data)


@app.route('/learn')
def learn_index():
    city_name = u'上海'

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': city_name,
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'learn'
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('learn/index.html', **data)


@app.route('/map')
def map_index():
    city_name = u'上海'

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': city_name,
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'map'
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('map/index.html', **data)


@app.route('/api')
def api_index():
    city_name = u'上海'

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default='')
    date_end = request.args.get('date_end', default='')
    city_name = request.args.get('city_name', default='')

    condition = {

    }
    other = {
        'city_name': city_name,
    }
    page = request.args.get('page', 1, type=int)
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31, other)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'api'
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('api/index.html', **data)

