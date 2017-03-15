# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String, Table, text
from sqlalchemy.sql.sqltypes import NullType
from database import db


Base = db.Model
metadata = Base.metadata


def to_dict(self):
    """
    model 对象转 字典
    model_obj.to_dict()
    """
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict


