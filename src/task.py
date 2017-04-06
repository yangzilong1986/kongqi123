# coding:utf-8
import datetime
import json
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI_MYSQL, SQLALCHEMY_POOL_SIZE
from web.www.core.history import History
from web.www.core.learn import Learn
from web.www.core.spider import Spider
from web.www.core.weather import Weather
from web.www.core.crawl import Crawl


def init_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE)
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = db_session()
    return session


def run_export_spider_job(current_date=''):
    current = datetime.datetime.now()
    if current_date:
        current = datetime.datetime.strptime(current_date, '%Y-%m')

    crawl_client = Crawl.factory()

    history_spider = 'aqistudy'
    history_client = History.factory()
    history_cities = history_client.get_history_city_all()
    if not history_cities:
        print 'no history city'
        return
    for city in history_cities:
        name = city['city_name']
        history_job = crawl_client.get_crawl_job_info(name, current.year, current.month, history_spider)
        if history_job:
            print 'job existed! city: %s, type, %d' % (name, Crawl.JOB_TYPE_HISTORY, )
            continue
        data = {
            'city_name': name,
            'job_year': current.year,
            'job_month': current.month,
            'job_spider': history_spider,
            'job_type': Crawl.JOB_TYPE_HISTORY,
            'job_status': Crawl.JOB_STATUS_READY,
        }
        if not crawl_client.create_crawl_job_info(data):
            print 'create job failed! city: %s, type, %d' % (name, Crawl.JOB_TYPE_HISTORY, )
        print 'create job success! city: %s, type, %d' % (name, Crawl.JOB_TYPE_HISTORY, )

    weather_spider = 'tianqihoubao'
    weather_client = Weather.factory()
    weather_cities = weather_client.get_weather_city_all()
    if not weather_cities:
        print 'no weather city'
        return
    for city in weather_cities:
        name = city['city_name']
        history_job = crawl_client.get_crawl_job_info(name, current.year, current.month, weather_spider)
        if history_job:
            print 'job existed! city: %s, type, %d' % (name, Crawl.JOB_TYPE_WEATHER, )
            continue
        data = {
            'city_name': name,
            'job_year': current.year,
            'job_month': current.month,
            'job_spider': weather_spider,
            'job_type': Crawl.JOB_TYPE_WEATHER,
            'job_status': Crawl.JOB_STATUS_READY,
        }
        if not crawl_client.create_crawl_job_info(data):
            print 'create job failed: city: %s, type, %d' % (name, Crawl.JOB_TYPE_WEATHER, )
        print 'create job success! city: %s, type, %d' % (name, Crawl.JOB_TYPE_WEATHER, )


def run_do_spider_job(current_date=''):
    current = datetime.datetime.now()
    if current_date:
        current = datetime.datetime.strptime(current_date, '%Y-%m')

    sp = Spider.factory()
    crawl_client = Crawl.factory()

    all_job = crawl_client.get_all_job({
        'job_year': current.year,
        'job_month': current.month,
    })
    if not all_job:
        print 'not job list'
        return

    for job_info in all_job:
        m = job_info['job_month']
        if int(m) < 10:
            m = '0' + str(m)
        month = str(job_info['job_year']) + '-' + str(m)

        result = sp.schedule_job(spider=job_info['job_spider'], setting=[],
                                 jobid=job_info['job_id'], city_name=job_info['city_name'], month=month)
        print job_info, result
        if not result:
            print u'启动任务失败!'
            continue
        # break


def my_job():
    print time.time()


def run_learn():
    learn_client = Learn.factory()
    learn_info = learn_client.get_learn_new_job_info()
    if not learn_info:
        # print 'no learn info skip'
        return False

    print learn_info

    if 'city_name' not in learn_info or len(learn_info['city_name']) < 1:
        learn_error(learn_info['learn_id'], '缺少城市名称')
        return False

    if 'date_start' not in learn_info:
        learn_error(learn_info['learn_id'], '缺少开始日期')
        return False

    if 'date_end' not in learn_info:
        learn_error(learn_info['learn_id'], '缺少结束日期')
        return False

    history_data = []
    if learn_info['history'] == 1:
        _history_data = learn_client.get_history_data(learn_info['city_name'], learn_info['date_start'], learn_info['date_end'])
        if _history_data:
            history_data = _history_data

    weather_data = []
    if learn_info['weather'] == 1:
        _weather_data = learn_client.get_weather_data(learn_info['city_name'], learn_info['date_start'], learn_info['date_end'])
        if _weather_data:
            weather_data = _weather_data

    data = []
    if learn_info['history'] == 1 and learn_info['weather'] == 1:
        if len(history_data) != len(weather_data):
            learn_error(learn_info['learn_id'], '选择了天气和空气数据，但两者数据量不匹配。')
            return False
        for index, item in enumerate(history_data):
            item = dict(history_data[index].items() + weather_data[index].items())
            # print item
            data.append(item)
        data = history_data
        # todo

    elif learn_info['history'] == 1:
        data = history_data
    elif learn_info['weather'] == 1:
        data = weather_data

    if not data:
        learn_error(learn_info['learn_id'], '缺少基本的数据')
        return False
    # print data

    histories = []
    _histories = learn_info['histories']
    if _histories:
        histories = json.loads(_histories)

    weathers = []
    _weathers = learn_info['weathers']
    if _weathers:
        weathers = json.loads(_weathers)

    key_list = histories + weathers
    if not key_list:
        learn_error(learn_info['learn_id'], '没有特征数据')
        return False
    # print key_list

    result = learn_client.output_tree(learn_info['learn_id'], data, key_list)
    print result

    learn_ok(learn_info['learn_id'], result[0], '/static/data/' + str(learn_info['learn_id']) + '.png')

    print 'one learn finished'


def learn_error(learn_id, error):
    learn_client = Learn.factory()
    data = {
        'learn_status': Learn.JOB_ERROR,
        'output_result': error
    }
    return learn_client.update_learn_info_by_id(learn_id, data)


def learn_ok(learn_id, result, output_file1):
    learn_client = Learn.factory()
    data = {
        'learn_status': Learn.JOB_FINISH,
        'output_result': json.dumps(result),
        'output_file1': output_file1
    }
    return learn_client.update_learn_info_by_id(learn_id, data)


def run_crontab():
    # schedule.every(10).minutes.do(run_export_service)
    print 'crontab'

    engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE)
    jobstores = {
        'sqlalchemy': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI_MYSQL, engine=engine),
        'default': MemoryJobStore()
    }
    executors = {
        'default': ThreadPoolExecutor(10),
        'processpool': ProcessPoolExecutor(3)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    # scheduler.add_job(my_job, 'interval', seconds=5)
    # scheduler.add_job(my_job, 'cron', year='*', month='*', day='*', hour='*', minute='*', second='*')
    scheduler.add_job(run_export_spider_job, 'cron', year='*', month='*', day=1, hour=1, minute=1, second=1)
    scheduler.add_job(run_learn, 'cron', year='*', month='*', day='*', hour='*', minute='*', second='*')
    scheduler.add_job(run_do_spider_job, 'cron', year='*', month='*', day='*', hour=22, minute=0, second=0)

    scheduler.start()


if __name__ == '__main__':
    from web.runhelp import main

    main(__file__, __name__)
