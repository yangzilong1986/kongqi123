# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from collections import defaultdict
# iris 值物分类
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

# 数据切分为train和test
# from sklearn.cross_validation import cross_val_score, train_test_split
# Use:func:`sklearn.model_selection.cross_val_score` instead.
# Use:func:`sklearn.model_selection.train_test_split` instead.
from sklearn.model_selection import train_test_split

# 指标来评估模型
from sklearn import metrics

# 交叉验证来评估模型
# from sklearn import cross_validation
# Use :func:`sklearn.model_selection.cross_val_score` instead.
from sklearn.model_selection import cross_val_score

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
        if data:
            _data = []
            for row in data:
                row = dict(row.items())
                _data.append(row)
            data = _data
        return data

    def test_simple_tree(self, city_name, start_date, end_date):
        '''
        for index, row in df.iterrows():
            row['level'] = 1
            if row['hd_pm25'] > 35:
                row['level'] = 2
            elif row['hd_pm25'] > 75:
                row['level'] = 3
            elif row['hd_pm25'] > 115:
                row['level'] = 4
            elif row['hd_pm25'] > 150:
                row['level'] = 4
            elif row['hd_pm25'] > 250:
                row['level'] = 5
            elif row['hd_pm25'] > 500:
                row['level'] = 6

        print df['hd_pm25']
        print df.dtypes

        clf = DecisionTreeClassifier(random_state=14)
        x_pm25 = df[['hd_pm25']].values
        # x_pm25 = df[['level_1', 'level_2', 'level_3', 'level_4', 'level_5', 'level_6']].values
        # print x_pm25
        y_true = df['level'].values
        print y_true
        scores = cross_val_score(clf, x_pm25, y_true, scoring='accuracy')
        print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))

        df1 = load_iris()
        x = df1.data
        y = df1.target

        print x
        print y


        for index, row in df.iterrows():
            if row['hd_pm25'] <= 35:
                row['level'] = 1
            elif 35 < row['hd_pm25'] <= 75:
                row['level'] = 2
            elif 75 < row['hd_pm25'] <= 115:
                row['level'] = 3
            elif 115 < row['hd_pm25'] <= 150:
                row['level'] = 4
            elif 150 < row['hd_pm25'] <= 250:
                row['level'] = 5
            elif row['hd_pm25'] > 250:
                row['level'] = 6

            # print index, row['hd_pm25'], row['level']
            df[index]['level'] = row['level']
            print "%s\t PM.5: %s,\t %s\t %s,\t %s,\t %s,\t %s,\t %s,\t %s" % (
                index,
                row['hd_pm25'],
                row['level'],
                row['level_1'],
                row['level_2'],
                row['level_3'],
                row['level_4'],
                row['level_5'],
                row['level_6'],
            )
        print df.dtypes

        # 使用更多指标来评估模型
        # def measure_performance(X, y, clf, show_accuracy=True, show_classification_report=True, show_confusion_matrix=True):
        # measure_performance(x_test, y_test, clf, show_classification_report=True, show_confusion_matrix=True)
        # x = x_test
        # y = y_test
        y_pred = clf.predict(x)
        print "Accuracy:{0:.3f}".format(metrics.accuracy_score(y, y_pred))

        print "Classification report"
        print metrics.classification_report(y, y_pred)

        print "Confusion matrix"
        print metrics.confusion_matrix(y, y_pred)

        # 交叉验证来评估模型
        scores = cross_val_score(clf, x, y, scoring='accuracy', cv=10)
        print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
        '''

        city_info = self.get_city_info_by_name(city_name)
        if not city_info:
            print u'不存在的城市: %s' % (city_name, )
            return

        city_id = city_info['city_id']
        data = self.load_daily_city_data(city_id, start_date, end_date)
        if not data:
            print u'城市没有数据: %s' % (city_name, )
            return

        # print type(data)

        for row in data:
            if row['hd_pm25'] <= 35:
                row['level'] = 1
            elif 35 < row['hd_pm25'] <= 75:
                row['level'] = 2
            elif 75 < row['hd_pm25'] <= 115:
                row['level'] = 3
            elif 115 < row['hd_pm25'] <= 150:
                row['level'] = 4
            elif 150 < row['hd_pm25'] <= 250:
                row['level'] = 5
            elif row['hd_pm25'] > 250:
                row['level'] = 6

        df = pd.DataFrame(data, columns=data[0].keys())
        df['hd_date'] = pd.to_datetime(df['hd_date'])
        df['hd_pm25'] = df['hd_pm25'].astype(np.double)
        df['hd_pm10'] = df['hd_pm10'].astype(np.double)
        df['hd_so2'] = df['hd_so2'].astype(np.double)
        df['hd_co'] = df['hd_co'].astype(np.double)
        df['hd_no2'] = df['hd_no2'].astype(np.double)
        df['hd_o3'] = df['hd_o3'].astype(np.double)

        df['level_1'] = df['hd_pm25'] <= 35
        df['level_2'] = (df['hd_pm25'] > 35) & (df['hd_pm25'] <= 75)
        df['level_3'] = (df['hd_pm25'] > 75) & (df['hd_pm25'] <= 115)
        df['level_4'] = (df['hd_pm25'] > 115) & (df['hd_pm25'] <= 150)
        df['level_5'] = (df['hd_pm25'] > 150) & (df['hd_pm25'] <= 250)
        df['level_6'] = df['hd_pm25'] > 250

        # print df

        subdf = df[['level', 'hd_pm25', 'hd_date']]
        y = df['level'].values

        # sklearn中的Imputer也可以
        hd_pm25 = subdf['hd_pm25'] # .fillna(value=subdf.age.mean())
        # hd_date = subdf['hd_date'] # (subdf['sex'] == 'male').astype('int')
        # sklearn OneHotEncoder也可以
        pclass = pd.get_dummies(subdf['level'], prefix='level')

        x = pd.concat([pclass, hd_pm25], axis=1) # hd_date
        x.head()
        print x

        # 切分测试和训练数据
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=14) #  test_size=0.25,

        # 决策树
        # clf = DecisionTreeClassifier(criterion='entropy', max_depth=3, min_samples_leaf=5)
        clf = DecisionTreeClassifier(criterion='gini')

        # 学习
        clf = clf.fit(x_train, y_train)
        print "准确率为：{:.2f}".format(clf.score(x_test, y_test))

        # 预测结果
        predict_target = clf.predict(x_test)
        # print x_test
        print predict_target
        # sum(predict_target == x)  # 预测成功的数量
        # result = clf.predict(digits.data[-1])


if __name__ == '__main__':
    """
    PM2.5 中国标准
    0-35    一级 优
    35-75   二级 良
    75-115  三级 轻度污染
    115-150 四级 中度污染
    150-250 五级 重度污染
    250-500 六级 严重污染

    PM2.5 美国标题
    0-12    一级 优
    12-35   二级 良
    35-55   三级 轻度污染
    55-150  四级 中度污染
    150-250 五级 重度污染
    250-500 六级 严重污染
    """

    demo = Demo()
    demo.test_simple_tree(u'上海', '2016-01-01', '2016-12-31')
