# coding:utf-8

import datetime
import time
import json
from flask import Flask, render_template, request, redirect, url_for, send_file, g, session, Response
from os.path import dirname, abspath
from core.history import History
from core.weather import Weather
from core.yahoo import Yahoo
from core.spider import Spider
from core.crawl import Crawl

STATIC_PATH = abspath(dirname(abspath(__file__)) + '/../static/')

app = Flask(__name__, static_folder=STATIC_PATH)
app.config.from_object('config.MainConfig')


@app.before_request
def before_request():
    # @todo 首页当前城市
    g.city_name = u'上海'
    if 'city_name' in session:
        g.city_name = session['city_name']


@app.route('/city')
def city_index():
    city_name = g.city_name
    weather_client = Weather.factory()

    name = request.args.get('name', default='')
    if name:
        city_info = weather_client.get_city_by_name(name)
        # print city_info
        if city_info:
            session['city_name'] = city_info['city_name']
            return redirect('/?city=%s' % city_info['city_name'])

    cities = weather_client.get_group_weather_city()

    data = dict()
    data['current_page'] = 'city'
    data['city_name'] = city_name
    data['req_args'] = dict(request.args.items())
    data['cities'] = cities

    return render_template('city.html', **data)


@app.route('/')
def index():
    # @todo 切换城市
    city = request.args.get('city', default='')

    city_name = g.city_name
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


@app.route('/data', methods=['GET', 'POST'])
def data_index():
    city_name = g.city_name

    history_client = History.factory()
    history_city = history_client.get_city_by_name(city_name)

    weather_client = Weather.factory()
    weather_city = weather_client.get_city_by_name(city_name)

    crawl_client = Crawl.factory()

    if request.method == 'POST':
        job_id = request.form.get('job_id', default=0)
        if not job_id:
            return json.dumps({'status': False, 'message': u'没有任务id!'})

        job_info = crawl_client.get_job_info_by_id(job_id)
        if not job_info:
            return json.dumps({'status': False, 'message': u'没有任务信息!'})
        if 'city_name' not in job_info or job_info['city_name'] != city_name:
            return json.dumps({'status': False, 'message': u'此城市没有任务信息!'})

        # scrapy crawl aqistudy -a city_name=上海 -a month=2017-01
        sp = Spider.factory()
        m = job_info['job_month']
        if int(m) < 10:
            m = '0' + str(m)
        month = str(job_info['job_year']) + '-' + str(m)

        result = sp.schedule_job(spider=job_info['job_spider'], setting=[], jobid=job_id, city_name=city_name, month=month)
        if not result:
            return json.dumps({'status': False, 'message': u'启动任务失败!'})
        return json.dumps({'status': True, 'message': u'启动任务成功!'})

    current = datetime.datetime.now()
    job_list = crawl_client.get_job_list(city_name, current.year, current.month)
    # print job_list

    data = dict()
    data['current_page'] = 'data'
    data['history_city'] = history_city
    data['weather_city'] = weather_city
    data['req_args'] = dict(request.args.items())
    data['job_list'] = job_list

    return render_template('data/index.html', **data)


@app.route('/data/job', methods=['POST'])
def data_job():
    city_name = g.city_name

    job_id = request.form.get('job_id', default=0)
    if not job_id:
        return json.dumps({'status': False, 'message': u'没有任务id!'})

    crawl_client = Crawl.factory()
    job_info = crawl_client.get_job_info_by_id(job_id)
    if not job_info:
        return json.dumps({'status': False, 'message': u'没有任务信息!'})
    if 'city_name' not in job_info or job_info['city_name'] != city_name:
        return json.dumps({'status': False, 'message': u'此城市没有任务信息!'})

    return json.dumps({'status': True, 'message': job_info['job_status']})


@app.route('/data/history')
def data_history():
    city_name = g.city_name

    history_client = History.factory()
    history_city = history_client.get_city_by_name(city_name)
    if not history_city:
        return u'暂时不支持此城市的天气数据查询'

    weather_client = Weather.factory()
    weather_city = weather_client.get_city_by_name(city_name)

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }
    history_client = History.factory()
    info = history_client.search_day(condition, page, 31)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    # print str(info)

    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'data'
    data['date_start'] = date_start
    data['date_end'] = date_end
    data['history_city'] = history_city
    data['weather_city'] = weather_city
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('data/history.html', **data)


@app.route('/data/weather')
def data_weather():
    city_name = g.city_name

    history_client = History.factory()
    history_city = history_client.get_city_by_name(city_name)

    weather_client = Weather.factory()
    weather_city = weather_client.get_city_by_name(city_name)
    if not weather_city:
        return u'暂时不支持此城市的AQI数据查询'

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    page = request.args.get('page', 1, type=int)
    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }

    weather_client = Weather.factory()
    info = weather_client.search_day(condition, page, 31)
    # print json.dumps(dict(info), indent=7, ensure_ascii=False)
    # print str(info)
    info['pages'] = min(7, info['pages'])

    data = dict()
    data['current_page'] = 'data'
    data['date_start'] = date_start
    data['date_end'] = date_end
    data['history_city'] = history_city
    data['weather_city'] = weather_city
    data['req_args'] = dict(request.args.items())
    data['info'] = info
    data['page'] = page

    return render_template('data/weather.html', **data)


@app.route('/report')
def report_index():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }
    weather_client = Weather.factory()
    weather_am = weather_client.total_weather(condition, 'weather_am')
    weather_pm = weather_client.total_weather(condition, 'weather_pm')
    # print weather_am
    # print weather_pm
    weather_am_wind_type = weather_client.total_weather(condition, 'weather_am_wind_type')
    weather_pm_wind_type = weather_client.total_weather(condition, 'weather_pm_wind_type')

    weather_am_wind_level = weather_client.total_weather(condition, 'weather_am_wind_level')
    weather_pm_wind_level = weather_client.total_weather(condition, 'weather_pm_wind_level')

    data = dict()
    data['current_page'] = 'report'
    data['req_args'] = dict(request.args.items())
    data['weather_am'] = weather_am
    data['weather_pm'] = weather_pm
    data['weather_am_wind_type'] = weather_am_wind_type
    data['weather_pm_wind_type'] = weather_pm_wind_type
    data['weather_am_wind_level'] = weather_am_wind_level
    data['weather_pm_wind_level'] = weather_pm_wind_level
    data['city_name'] = city_name
    data['date_start'] = date_start
    data['date_end'] = date_end

    return render_template('report/index.html', **data)


@app.route('/report/aqi_total')
def report_aqi_total():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }
    history_client = History.factory()
    hd_quality = history_client.total_history(condition, 'hd_quality')

    data = dict()
    data['current_page'] = 'report'
    data['req_args'] = dict(request.args.items())
    data['hd_quality'] = hd_quality
    data['city_name'] = city_name
    data['date_start'] = date_start
    data['date_end'] = date_end

    return render_template('report/aqi_total.html', **data)


@app.route('/report/weather_trend')
def report_weather_trend():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }
    weather_client = Weather.factory()
    weather_all = weather_client.all_day(condition)
    weather_am_types = weather_client.total_types(condition, 'weather_am')
    weather_pm_types = weather_client.total_types(condition, 'weather_pm')
    weather_am_wind_types = weather_client.total_types(condition, 'weather_am_wind_type')
    weather_pm_wind_types = weather_client.total_types(condition, 'weather_pm_wind_type')
    weather_am_level_types = weather_client.total_types(condition, 'weather_am_wind_level')
    weather_pm_level_types = weather_client.total_types(condition, 'weather_pm_wind_level')

    for weather in weather_all:
        weather['weather_am_index'] = weather_am_types.index(weather['weather_am'])
        weather['weather_pm_index'] = weather_pm_types.index(weather['weather_pm'])
        weather['weather_am_wind_index'] = weather_am_wind_types.index(weather['weather_am_wind_type'])
        weather['weather_pm_wind_index'] = weather_pm_wind_types.index(weather['weather_pm_wind_type'])
        weather['weather_am_level_index'] = weather_am_level_types.index(weather['weather_am_wind_level'])
        weather['weather_pm_level_index'] = weather_pm_level_types.index(weather['weather_pm_wind_level'])

    data = dict()
    data['current_page'] = 'report'
    data['req_args'] = dict(request.args.items())
    data['weather_all'] = weather_all
    data['city_name'] = city_name
    data['date_start'] = date_start
    data['date_end'] = date_end

    return render_template('report/weather_trend.html', **data)


@app.route('/report/aqi_trend')
def report_aqi_trend():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }
    history_client = History.factory()
    history_all = history_client.all_day(condition)
    history_types = [
        u'优',
        u'良',
        u'轻度污染',
        u'中度污染',
        u'重度污染',
        u'严重污染'
    ]
    for history in history_all:
        history['hd_quality_index'] = history_types.index(history['hd_quality'])

    data = dict()
    data['current_page'] = 'report'
    data['req_args'] = dict(request.args.items())
    data['history_all'] = history_all
    data['city_name'] = city_name
    data['date_start'] = date_start
    data['date_end'] = date_end

    return render_template('report/aqi_trend.html', **data)


@app.route('/learn')
def learn_index():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)
    history = request.args.get('history', default=1, type=int)
    weather = request.args.get('weather', default=1, type=int)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }

    history_client = History.factory()
    weather_client = Weather.factory()
    history_count = 0
    weather_count = 0
    if history == 1:
        history_count = history_client.count_history(condition)
    if weather == 1:
        weather_count = weather_client.count_weather(condition)

    data = dict()
    data['current_page'] = 'learn'
    data['req_args'] = dict(request.args.items())
    data['city_name'] = city_name
    data['date_start'] = date_start
    data['date_end'] = date_end
    data['history'] = history
    data['weather'] = weather
    data['history_count'] = history_count
    data['weather_count'] = weather_count

    return render_template('learn/index.html', **data)


@app.route('/learn/step2')
def learn_step2():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)
    history = request.args.get('history', default=1, type=int)
    weather = request.args.get('weather', default=1, type=int)

    condition = {
        'city_name': city_name,
        'date_start': date_start,
        'date_end': date_end
    }

    history_client = History.factory()
    weather_client = Weather.factory()
    history_count = 0
    weather_count = 0
    if history == 1:
        history_count = history_client.count_history(condition)
    if weather == 1:
        weather_count = weather_client.count_weather(condition)

    data = dict()
    data['current_page'] = 'learn'
    data['req_args'] = dict(request.args.items())
    data['city_name'] = city_name
    data['date_start'] = date_start
    data['date_end'] = date_end
    data['history'] = history
    data['weather'] = weather
    data['history_count'] = history_count
    data['weather_count'] = weather_count

    return render_template('learn/step2.html', **data)


@app.route('/learn/image')
def learn_image():

    import pandas as pd
    import numpy as np
    import pydotplus
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.tree import export_graphviz

    city_name = g.city_name

    start_date = '2016-01-01'
    end_date = '2016-12-31'

    history_client = History.factory()
    weather_client = Weather.factory()

    city_info = history_client.get_city_by_name(city_name)
    if not city_info:
        print u'不存在的城市: %s' % (city_name, )
        return

    weather_city = weather_client.get_city_by_name(city_name)
    if not city_info:
        print u'不存在的天气数据城市: %s' % (city_name, )
        return

    city_id = city_info['city_id']
    aqi_data = history_client.load_daily_city_data(city_id, start_date, end_date)
    if not aqi_data:
        print u'城市没有数据: %s' % (city_name, )
        return

    weather_city_id = weather_city['city_id']
    weather_data = weather_client.load_daily_weather_data(weather_city_id, start_date, end_date)
    if not weather_data:
        print u'城市没有数据: %s' % (city_name, )
        return

    for row in aqi_data:
        if row['hd_quality'] == u'优':
            row['level'] = 1
        elif row['hd_quality'] == u'良':
            row['level'] = 2
        elif row['hd_quality'] == u'轻度污染':
            row['level'] = 3
        elif row['hd_quality'] == u'中度污染':
            row['level'] = 4
        elif row['hd_quality'] == u'重度污染':
            row['level'] = 5
        elif row['hd_quality'] == u'严重污染':
            row['level'] = 6

    df = pd.DataFrame(aqi_data, columns=aqi_data[0].keys())
    df['hd_date'] = pd.to_datetime(df['hd_date'])
    df['hd_pm25'] = df['hd_pm25'].astype(np.double)
    df['hd_pm10'] = df['hd_pm10'].astype(np.double)
    df['hd_so2'] = df['hd_so2'].astype(np.double)
    df['hd_co'] = df['hd_co'].astype(np.double)
    df['hd_no2'] = df['hd_no2'].astype(np.double)
    df['hd_o3'] = df['hd_o3'].astype(np.double)

    x = df[['hd_pm10', 'hd_so2', 'hd_co', 'hd_no2', 'hd_o3']].values
    y = df['hd_pm25'].values

    x_test = [
        [48.2, 19.3, 0.858, 65.8, 80],  # 33.4,
        [72.3, 22, 1.171, 66.8, 68],  # 66.8,
        [106.2, 17.6, 1.25, 71.5, 85],  # 96.5,
    ]

    clf = DecisionTreeRegressor()
    clf = clf.fit(x, y)
    y_1 = clf.predict(x_test)

    feature_names = ['hd_pm10', 'hd_so2', 'hd_co', 'hd_no2', 'hd_o3']
    target_names = ['hd_pm25']

    dot_data = export_graphviz(clf, out_file=None, feature_names=feature_names, class_names=target_names,
                               filled=True, rounded=True, special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)
    temp = graph.create_png()
    print type(temp)

    # response = send_file(temp, as_attachment=True, attachment_filename='myfile.png')
    # response = send_file(temp, mimetype='image/png')

    return Response(temp, mimetype='image/png')


@app.route('/map')
def map_index():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    date_end = request.args.get('date_end', default=today)
    hd_type = request.args.get('type', default='aqi')

    condition = {
        'date': date_end,
    }
    hd_types = ['aqi', 'quality', 'pm25', 'pm10', 'so2', 'co', 'no2', 'o3']
    if hd_type not in hd_types:
        hd_type = 'aqi'

    field = 'hd_' + hd_type
    history_client = History.factory()
    city_all = history_client.all_city(condition)

    data = dict()
    data['current_page'] = 'map'
    data['city_name'] = city_name
    data['city_all'] = city_all
    data['req_args'] = dict(request.args.items())
    data['date_end'] = date_end
    data['type'] = hd_type
    data['field'] = field

    return render_template('map/index.html', **data)


@app.route('/api')
def api_index():
    return

