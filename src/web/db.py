#!/usr/bin/env python
# encoding: utf-8

# db.init_app(app)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI,DB_PARAMS
from tools.json_encoder import ok

ok()

engine = create_engine(SQLALCHEMY_DATABASE_URI, **DB_PARAMS)
DB_Session = sessionmaker(bind=engine, autocommit=True)

import logging
log = logging.getLogger('api')


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


def get_session():
    return session_context(DB_Session())


from api.models import Base

Base.metadata.create_all(engine)


if __name__ == '__main__':
    pass
