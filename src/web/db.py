#!/usr/bin/env python
# encoding: utf-8

# db.init_app(app)
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI_MYSQL, SQLALCHEMY_POOL_SIZE
from spider.model import Base

log = logging.getLogger('db')
db_params = dict(
    echo=False,
    echo_pool=True,
    # encoding=db_config['charset'],
    pool_recycle=1800,  # 数据库链接时间
    pool_size=20,
    logging_name='sqlalchemy',
)
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, **db_params)
    # DB_Session = sessionmaker(bind=engine, autocommit=True)
    # DB_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base.metadata.create_all(engine)
except Exception, e:
    print e.message
    exit()


def create_conn():
    conn = engine.connect()
    return conn


class get_new_db(object):
    """
    获取游标 实例
    """

    def __init__(self):
        self.conn = create_conn()

    def __enter__(self):
        """
        :return:
        :type:(MySQLdb.Connection, MySQLdb.cursors.DictCursor)
        """
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):

        try:
            self.conn.close()
        except Exception as e:
            log.exception(e)


class session_context(object):
    """
    db
    session 会话管理
    """

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        # 是否开启会话
        # self.session.begin()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
        except Exception as e:
            log.error('error:%s' % (e.message,))


# def get_session():
#    return session_context(DB_Session())


if __name__ == '__main__':
    pass
