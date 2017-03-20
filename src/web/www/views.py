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
from core.learn import Learn
# from server import app
# from run import app
from web.www import create_app
app = create_app()


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


@app.route('/learn/step2', methods=['GET', 'POST'])
def learn_step2():
    city_name = g.city_name

    today = time.strftime("%Y-%m-%d", time.localtime())
    day7_dt = datetime.datetime.now() - datetime.timedelta(days=7)
    day7 = day7_dt.strftime("%Y-%m-%d")

    date_start = request.args.get('date_start', default=day7)
    date_end = request.args.get('date_end', default=today)
    history = request.args.get('history', default=1, type=int)
    weather = request.args.get('weather', default=1, type=int)
    day_num = request.args.get('day_num', default=1, type=int)

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

    if request.method == 'POST':
        histories = request.form.getlist('histories[]')
        weathers = request.form.getlist('weathers[]')
        # print histories, weathers
        if not histories and not weathers:
            return json.dumps({'status': False, 'message': u'请您勾选特征数据类型!'})

        if history_count < 1 and weather_count < 1:
            return json.dumps({'status': False, 'message': u'选定的日期内没有数据,请返回上一步重新选择!'})
        if (history_count + weather_count) < 7:
            return json.dumps({'status': False, 'message': u'数据至少应该有7条(天)以上才能进行机器学习!'})

        learn_client = Learn.factory()
        job_id = learn_client.create_job({
            'learn_status': Learn.JOB_READY,
            'city_name': city_name,
            'date_start': date_start,
            'date_end': date_end,
            'history': history,
            'weather': weather,
            'histories': json.dumps(histories),
            'weathers': json.dumps(weathers),
            'target': 'PM25',
            'day_num': day_num
        })
        if not job_id:
            return json.dumps({'status': False, 'message': u'建立机器学习任务失败!'})

        return json.dumps({'status': True, 'message': job_id})

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


@app.route('/learn/step3', methods=['GET', 'POST'])
def learn_step3():
    city_name = g.city_name
    learn_client = Learn.factory()

    if request.method == 'POST':
        learn_id = request.form.get('learn', type=int)
        if not learn_id:
            return json.dumps({'status': False, 'message': u'没有learn_id!'})

        learn_info = learn_client.get_learn_info_by_id(learn_id)
        if not learn_info:
            return json.dumps({'status': False, 'message': u'没有learn_info!'})

        if learn_info['learn_status'] == Learn.JOB_ERROR:
            return json.dumps({'status': True, 'message': learn_info['learn_status'], 'result': learn_info['output_result']})
        if learn_info['learn_status'] == Learn.JOB_FINISH:
            return json.dumps({'status': True, 'message': learn_info['learn_status'], 'result': learn_info['output_result']})

        return json.dumps({'status': False, 'message': learn_info['learn_status']})

    learn_id = request.args.get('learn', type=int)
    if not learn_id:
        return redirect('/learn')

    learn_info = learn_client.get_learn_info_by_id(learn_id)
    if not learn_info:
        return redirect('/learn')

    data = dict()
    data['current_page'] = 'learn'
    data['req_args'] = dict(request.args.items())
    data['learn_info'] = learn_info
    data['city_name'] = city_name

    return render_template('learn/step3.html', **data)


@app.route('/learn/step4')
def learn_step4():
    city_name = g.city_name

    learn_id = request.args.get('learn', type=int)
    if not learn_id:
        return redirect('/learn')

    learn_client = Learn.factory()
    learn_info = learn_client.get_learn_info_by_id(learn_id)
    if not learn_info:
        return redirect('/learn')

    data = dict()
    data['current_page'] = 'learn'
    data['req_args'] = dict(request.args.items())
    data['city_name'] = city_name
    data['learn_info'] = learn_info

    return render_template('learn/step4.html', **data)


@app.route('/learn/image')
def learn_image():
    pass


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

