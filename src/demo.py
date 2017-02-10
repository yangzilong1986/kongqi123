# -*- coding: utf-8 -*-
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from collections import defaultdict
# iris 值物分类
from sklearn.datasets import load_iris
# 分类决策树
from sklearn.tree import DecisionTreeClassifier
# 回归决策树
from sklearn.tree import DecisionTreeRegressor

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

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report


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

        '''
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
        '''
        x = df[['hd_pm25']].values
        y = df['level'].values

        # 切分测试和训练数据
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=14) #  test_size=0.25,

        # 决策树
        # clf = DecisionTreeClassifier(criterion='entropy', max_depth=3, min_samples_leaf=5)
        clf = DecisionTreeClassifier(criterion='gini')

        # 学习
        clf = clf.fit(x_train, y_train)
        print "准确率为：{:.2f}".format(clf.score(x_test, y_test))

        # 结果
        predict_target = clf.predict(x_test)
        # print x_test
        print predict_target
        # sum(predict_target == x)  # 预测成功的数量
        # result = clf.predict(digits.data[-1])
        print clf.predict_proba(x_test)

    def test_iris_tree(self):
        iris = load_iris()

        test_idx = [0, 50, 100]

        # training data
        train_target = np.delete(iris.target, test_idx)
        train_data = np.delete(iris.data, test_idx, axis=0)

        # testing data

        test_target = iris.target[test_idx]
        test_data = iris.data[test_idx]

        clf = DecisionTreeClassifier()
        clf.fit(train_data, train_target)

        print test_target  # ground truth label of test data
        print clf.predict(test_data)  # the prediction of decision tree

    def test_show_iris_tree(self):
        """
        from sklearn.externals.six import StringIO
        import pydot
        dot_data = StringIO()
        tree.export_graphviz(clf, out_file=dot_data,
                             feature_names=iris.feature_names,
                             class_names=iris.target_names,
                             filled=True, rounded=True,
                             impurity=False)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph[0].write_pdf("iris.pdf")
        :return:
        """

    def test_iris_tree2(self):
        iris = load_iris()
        clf = DecisionTreeClassifier()
        clf = clf.fit(iris.data, iris.target)

        '''
        with open("iris.dot", 'w') as f:
            f = tree.export_graphviz(clf, out_file=f)
        import os
        os.unlink('iris.dot')

        import pydotplus
        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_pdf("iris.pdf")

        from IPython.display import Image
        dot_data = tree.export_graphviz(clf, out_file=None,
                                        feature_names = iris.feature_names,
                                        class_names = iris.target_names,
                                        filled = True, rounded = True,
                                        special_characters = True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        Image(graph.create_png())
        '''

        print clf.predict(iris.data[:1, :])
        print clf.predict_proba(iris.data[:1, :])

    def test_iris_forest(self):
        iris = load_iris()
        df = pd.DataFrame(iris.data, columns=iris.feature_names)
        df['is_train'] = np.random.uniform(0, 1, len(df)) <= .75
        # df['species'] = pd.Factor(iris.target, iris.target_names)
        df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
        print df.head()

        train, test = df[df['is_train'] == True], df[df['is_train'] == False]

        features = df.columns[:4]
        clf = RandomForestClassifier(n_jobs=2)
        y, _ = pd.factorize(train['species'])
        print y
        clf.fit(train[features], y)

        preds = iris.target_names[clf.predict(test[features])]
        print pd.crosstab(test['species'], preds, rownames=['actual'], colnames=['preds'])

    def test_titanic_tree(self):
        # from sklearn.cross_validation import train_test_split
        # from sklearn.tree import DecisionTreeClassifier

        titanic = pd.read_csv('http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt')
        titanic.head()
        titanic.info()

        X = titanic[['pclass', 'age', 'sex']]
        y = titanic['survived']
        X['age'].fillna(X['age'].mean(), inplace=True)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)

        vec = DictVectorizer(sparse=False)
        X_train = vec.fit_transform(X_train.to_dict(orient='record'))
        print vec.feature_names_

        X_test = vec.transform(X_test.to_dict(orient='record'))
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        y_predict = dtc.predict(X_test)

        print classification_report(y_predict, y_test, target_names=['died', 'survived'])

    def test_tree_classifier(self):
        """
        DecisionTreeClassifier 能够实现多类别的分类。
        输入两个向量：向量X，大小为[n_samples,n_features]，用于记录训练样本；
        向量Y，大小为[n_samples]，用于存储训练样本的类标签。
        :return:

        X = [[0, 0], [1, 1]]
        Y = [0, 1]
        clf = DecisionTreeClassifier()
        clf = clf.fit(X, Y)

        clf.predict([[2., 2.]])
        clf.predict_proba([[2., 2.]])
        """

        iris = load_iris()
        clf = DecisionTreeClassifier()
        clf = clf.fit(iris.data, iris.target)

        # export the tree in Graphviz format using the export_graphviz exporter
        with open("iris.dot", 'w') as f:
            f = tree.export_graphviz(clf, out_file=f)

        # predict the class of samples
        clf.predict(iris.data[:1, :])
        # the probability of each class
        clf.predict_proba(iris.data[:1, :])

    def test_tree_regressor(self):
        """
        和分类不同的是向量y可以是浮点数。

        :return:

        X = [[0, 0], [2, 2]]
        y = [0.5, 2.5]
        clf = DecisionTreeRegressor()
        clf = clf.fit(X, y)
        clf.predict([[1, 1]])

        predict：输出n个预测值
        predict_proba：输出有n个输出的向量组成的列表。

        apply(X[, check_input])	                    返回每个样本的叶节点的预测序号
        decision_path(X[, check_input])	            返回决策树的决策路径 [n_samples, n_nodes]
        fit(X, y[, sample_weight, check_input, …])	从训练数据建立决策树，返回一个对象
        fit_transform(X[, y])	                    将数据X转换[n_samples, n_features_new]
        get_params([deep])	                        得到估计量的参数，返回一个映射
        predict(X[, check_input])	                预测X的分类或者回归，返回[n_samples]
        predict_log_proba(X)	                    预测输入样本的对数概率，返回[n_samples, n_classes]
        predict_proba(X[, check_input])	            预测输入样本的属于各个类的概率[n_samples, n_classes]
        score(X, y[, sample_weight])	            返回对于测试数据的平均准确率
        set_params(**params)	                    设置估计量的参数
        transform(*args, **kwargs)	                将输入参数X减少的最重要的特征，返回[n_samples, n_selected_features]
        """

    def test_simple_tree2(self, city_name, start_date, end_date):
        """
        X = [[0, 0], [2, 2]]
        y = [0.5, 2.5]
        clf = DecisionTreeRegressor()
        clf = clf.fit(X, y)
        print clf.predict([[1, 1]])
        # [ 0.5]
        """

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

        x = df[['hd_pm25']].values
        y = df['level'].values

        clf = DecisionTreeRegressor()
        clf = clf.fit(x, y)
        print clf.predict([[35]])



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
    # demo.test_simple_tree(u'上海', '2016-01-01', '2016-12-31')
    # demo.test_iris_forest()
    # demo.test_iris_tree2()
    # demo.test_titanic_tree()
    demo.test_simple_tree2(u'上海', '2016-01-01', '2016-12-31')