# coding:utf-8
"""
工具方法
"""

from math import ceil


def get_page_count(total, page_size):
    return int(ceil(float(total) / min(1, page_size)))


def to_dict(row):
    return row.__dict__ if row else None


def to_list(rows):
    return [row.__dict__ for row in rows]


def insert_table(conn, table, row):
    sql = 'INSERT INTO `' + table + '`'
    keys = row.keys()
    sql += ' (' + (', '.join(['`%s`' % k for k in keys])) + ')'
    sql += 'values(' + ', '.join(['%s' for _ in keys]) + ')'
    param = [row[k] for k in keys]
    ret = conn.execute(sql, param)
    return ret.lastrowid


def update_table_row(conn, table, cond, row):
    sql = 'update `' + table + '` set '
    keys = row.keys()
    sql += (', '.join(['`%s`=%%s' % k for k in keys]))
    sql += ' where '
    sql += ' and '.join(['`%s`=%%s' % k for k in cond.keys()])
    param = [row[k] for k in keys]
    param += [cond[k] for k in cond]
    ret = conn.execute(sql, param)
    return ret.rowcount


def get_table_one_row(conn, table, condition):
    keys = condition.keys()
    where = ' and '.join('`%s`=%%s' % (k,) for k in keys)
    param = [condition[k] for k in keys]
    sql = 'select * from ' + table + ' where ' + where
    row = conn.execute(sql, param).fetchone()
    if row is not None:
        return dict(row)
    return None


class LikeValue(object):
    def __init__(self, value):
        self.value = value


def count_table(conn, table, condition):
    sql_where, params = make_where(condition)
    count_sql = 'SELECT count(*) AS c FROM `' + table + '` WHERE ' + sql_where
    count_row = conn.execute(count_sql, params).fetchone()
    return count_row['c']


def get_table_rows(conn, table, condition):
    keys = condition.keys()
    where = ' and '.join('`%s`=%%s' % (k,) for k in keys)
    param = [condition[k] for k in keys]
    sql = 'select * from ' + table + ' where ' + where
    # print sql
    return [dict(row) for row in conn.execute(sql, param).fetchall()]


def get_table_all(conn, table):
    sql = 'select * from ' + table
    return [dict(row) for row in conn.execute(sql).fetchall()]


def make_where(condition):
    keys = condition.keys()
    where = ' and '.join('`%s`=%%s' % (k,) for k in keys)
    return where, condition.values()


def make_where_with_table(table,condition):
    keys = condition.keys()
    where = ' and '.join('`%s`.`%s`=%%s' % (table,k,) for k in keys)
    return where, condition.values()


def get_table_count(conn, table, condition):
    keys = condition.keys()
    where = ' and '.join('`%s`=%%s' % (k,) for k in keys)
    param = [condition[k] for k in keys]
    sql = 'select count(*) as c from ' + table + ' where ' + where
    row = conn.execute(sql, param).fetchone()
    return row['c']
