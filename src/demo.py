# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
import pandas as pd
import numpy as np


class Demo(object):
    def __init__(self):
        try:
            self.engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE)
            self.db_session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.session = self.db_session()
        except Exception as e:
            print e.message
            exit()

    def get_city_info_by_id(self, city_id):
        row_sql = "select * from history_city where city_id = :city_id"
        row_data = {"city_id": city_id}
        row = self.session.execute(row_sql, row_data).fetchone()
        return row

    def get_city_info_by_name(self, city_name):
        row_sql = "select * from history_city where city_name = :city_name"
        row_data = {"city_name": city_name}
        row = self.session.execute(row_sql, row_data).fetchone()
        return row

    def load_daily_city_data(self, city_id, start_date, end_date):
        row_sql = "select * from history_day " \
                  "where city_id = :city_id and hd_date >= :start_date and hd_date <= :end_date"
        row_data = {"city_id": city_id, "start_date": start_date, "end_date": end_date}
        data = self.session.execute(row_sql, row_data).fetchall()
        return data

    def test_simple_tree(self, city_name, start_date, end_date):
        city_info = self.get_city_info_by_name(city_name)
        if not city_info:
            print '不存在的城市: %s' % (city_name, )
            return

        city_id = city_info['city_id']
        data = self.load_daily_city_data(city_id, start_date, end_date)
        if not data:
            print '城市没有数据: %s' % (city_name, )
            return

        df = pd.DataFrame(data, columns=data[0].keys())
        df['hd_date'] = pd.to_datetime(df['hd_date'])
        df['hd_pm25'] = df['hd_pm25'].astype(np.double)
        df['hd_pm10'] = df['hd_pm10'].astype(np.double)
        df['hd_so2'] = df['hd_so2'].astype(np.double)
        df['hd_co'] = df['hd_co'].astype(np.double)
        df['hd_no2'] = df['hd_no2'].astype(np.double)
        df['hd_o3'] = df['hd_o3'].astype(np.double)

        print df
        print df.dtypes

        '''
        clf = DecisionTreeClassifier(random_state=14)
        x_pm25 = df['hd_pm25'].values
        pm25 = cross_val_score(clf, pm25, y_true)
        '''

if __name__ == '__main__':
    demo = Demo()
    demo.test_simple_tree(u'上海', '2016-01-01', '2016-12-31')
