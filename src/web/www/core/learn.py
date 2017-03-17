# coding:utf-8

import pandas as pd
import numpy as np
import pydotplus
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import export_graphviz
import itertools

from web.www.core.history import History
from web.www.core.weather import Weather
from web.www.helper import *
from web.db import get_new_db


class Learn(object):

    JOB_READY = 1
    JOB_DOING = 2
    JOB_FINISH = 3
    JOB_ERROR = 4

    @staticmethod
    def factory():
        if hasattr(Learn, '_obj'):
            return Learn._obj

        obj = Learn()
        Learn._obj = obj

        return obj

    @staticmethod
    def get_learn_info_by_id(learn_id):
        with get_new_db() as conn:
            condition = {
                'learn_id': learn_id,
            }
            return get_table_one_row(conn, 'learn_job', condition)

    @staticmethod
    def get_learn_new_job_info():
        with get_new_db() as conn:
            sql = 'select * from learn_job where learn_status = 1 order by learn_id desc limit 1'
            info = conn.execute(sql).fetchone()
            return info

    @staticmethod
    def update_learn_info_by_id(learn_id, data):
        with get_new_db() as conn:
            return update_table_row(conn, 'learn_job', {'learn_id': learn_id}, data)

    @staticmethod
    def create_job(data):
        with get_new_db() as conn:
            return insert_table(conn, 'learn_job', data)

    @staticmethod
    def get_weather_data(city_name, start_date, end_date):
        weather_client = Weather.factory()
        weather_city = weather_client.get_city_by_name(city_name)
        if not weather_city:
            print u'不存在的天气数据城市: %s' % (city_name, )
            return []

        weather_city_id = weather_city['city_id']
        weather_data = weather_client.load_daily_weather_data(weather_city_id, start_date, end_date)
        if not weather_data:
            print u'城市没有数据: %s' % (city_name, )
            return []

        condition = {
            'city_name': city_name,
            'date_start': start_date,
            'date_end': end_date
        }
        weather_am_types = weather_client.total_types(condition, 'weather_am')
        weather_pm_types = weather_client.total_types(condition, 'weather_pm')
        weather_am_wind_types = weather_client.total_types(condition, 'weather_am_wind_type')
        weather_pm_wind_types = weather_client.total_types(condition, 'weather_pm_wind_type')
        weather_am_level_types = weather_client.total_types(condition, 'weather_am_wind_level')
        weather_pm_level_types = weather_client.total_types(condition, 'weather_pm_wind_level')

        for weather in weather_data:
            weather['weather_am_index'] = weather_am_types.index(weather['weather_am'])
            weather['weather_pm_index'] = weather_pm_types.index(weather['weather_pm'])
            weather['weather_am_wind_index'] = weather_am_wind_types.index(weather['weather_am_wind_type'])
            weather['weather_pm_wind_index'] = weather_pm_wind_types.index(weather['weather_pm_wind_type'])
            weather['weather_am_level_index'] = weather_am_level_types.index(weather['weather_am_wind_level'])
            weather['weather_pm_level_index'] = weather_pm_level_types.index(weather['weather_pm_wind_level'])

        return weather_data

    @staticmethod
    def get_history_data(city_name, start_date, end_date):
        history_client = History.factory()
        city_info = history_client.get_city_by_name(city_name)
        if not city_info:
            print u'不存在的城市: %s' % (city_name, )
            return []

        city_id = city_info['city_id']
        history_data = history_client.load_daily_city_data(city_id, start_date, end_date)
        if not history_data:
            print u'城市没有数据: %s' % (city_name, )
            return []

        for row in history_data:
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

        return history_data

    @staticmethod
    def output_tree(data, test, key_list):
        df = pd.DataFrame(data, columns=data[0].keys())

        if 'hd_date' in key_list:
            df['hd_date'] = pd.to_datetime(df['hd_date'])
        if 'hd_pm25' in key_list:
            df['hd_pm25'] = df['hd_pm25'].astype(np.double)
        if 'hd_pm10' in key_list:
            df['hd_pm10'] = df['hd_pm10'].astype(np.double)
        if 'hd_so2' in key_list:
            df['hd_so2'] = df['hd_so2'].astype(np.double)
        if 'hd_co' in key_list:
            df['hd_co'] = df['hd_co'].astype(np.double)
        if 'hd_no2' in key_list:
            df['hd_no2'] = df['hd_no2'].astype(np.double)
        if 'hd_o3' in key_list:
            df['hd_o3'] = df['hd_o3'].astype(np.double)

        x = df[key_list].values
        y = df['hd_pm25'].values

        '''
        x_test = [
            [48.2, 19.3, 0.858, 65.8, 80],  # 33.4,
            [72.3, 22, 1.171, 66.8, 68],  # 66.8,
            [106.2, 17.6, 1.25, 71.5, 85],  # 96.5,
        ]
        '''

        clf = DecisionTreeRegressor()
        clf = clf.fit(x, y)
        y_1 = clf.predict(x_test)

        feature_names = key_list
        target_names = ['hd_pm25']

        dot_data = export_graphviz(clf, out_file=None, feature_names=feature_names, class_names=target_names,
                                   filled=True, rounded=True, special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        temp = graph.create_png()
        print type(temp)

        # response = send_file(temp, as_attachment=True, attachment_filename='myfile.png')
        # response = send_file(temp, mimetype='image/png')

        # return Response(temp, mimetype='image/png')

