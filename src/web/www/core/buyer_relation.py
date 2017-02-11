# coding:utf-8

import logging

from api import helper
from api.helper import insert_table, update_table_row, get_table_one_row, make_where

log = logging.getLogger('api')


def get_relation_info(conn, uid, shop_id):
    """
    获取用户的代言关系
    :param uid:
    :return:
    """
    row = conn.execute('SELECT * FROM buyer_relation WHERE uid = %s AND shop_id = %s ',
                       (uid, shop_id)).fetchone()
    return row


def build_relation(conn, order_code):
    """
    建立代言关系.内部接口
    :param order_code:
    :return:
    """

    order_info = conn.execute('SELECT * FROM `order` WHERE order_code=%s LIMIT 1', (order_code,)).fetchone()

    if not order_info:
        log.info('order_code:%s, 订单不存在' % order_code)
        return False
    order_uid = order_info['buy_uid']
    order_shop_id = order_info['shop_id']
    # 检查重复(uid shop_id 联合索引)
    # 已经存在的关系
    buyer_relation_info = conn.execute('SELECT * FROM buyer_relation WHERE uid = %s AND shop_id = %s ',
                                       (order_uid, order_shop_id)).fetchone()

    if buyer_relation_info:
        log.info('order_code:%s,uid:%s,shop_id:%s 代言关系已经存在' % \
                 (order_code, order_uid, order_shop_id)
                 )
        return True
    p1_uid = 0
    p2_uid = 0

    if order_info['endorse_id']:
        # 代言信息
        from api.biz.endorse import EndorseApi
        endorse_info = EndorseApi.get_info({'id': order_info['endorse_id']})
        if endorse_info and endorse_info['shop_id'] == order_info['shop_id'] \
                and order_uid != endorse_info['uid']:
            p1_uid = endorse_info['uid']
            p2_uid = get_p1_uid(conn, endorse_info['uid'], order_shop_id)

    # 创建关系
    order_product_id = 0
    # 获取产品id
    import time
    buyer_relation_data = {
        'uid': order_uid,
        'shop_id': order_shop_id,
        'p1_uid': p1_uid,
        'p2_uid': p2_uid,
        'endorse_id': order_info['endorse_id'],
        'order_id': order_info['id'],
        'product_id': order_product_id,
        'create_time': time.time()
    }
    insert_table(conn, 'buyer_relation', buyer_relation_data)
    log.info('order_code:%s, add buyer_relation_data' % (order_code,))
    return True


def get(conn, buyer_relation_id):
    """
    根据主键获取买家关系
    :type conn: sqlalchemy.engine.base.Connection
    :param buyer_relation_id:
    :return:
    """

    return conn.execute('SELECT * FROM buyer_relation WHERE id=%s', (buyer_relation_id,)).fetchone()


def add(conn, info):
    """
    添加买家关系
    :type conn: sqlalchemy.engine.base.Connection
    :param info:
    :return:
    """
    return insert_table(conn, 'buyer_relation', info)


def edit(conn, relation_id, info):
    """
    修改买家关系
    :param relation_id:
    :param info:
    :return:
    """

    return update_table_row(conn, 'buyer_relation', {'id': relation_id}, info)


def delete(conn, relation_id):
    """
    删除代言关系
    """

    conn.execute('DELETE FROM buyer_relation WHERE id=%s LIMIT 1', (relation_id,))


def get_info(conn, condition):
    """
    根据条件获取买家关系
    """
    return get_table_one_row(conn, 'buyer_relation', condition)


def get_p1_uid(conn, uid, shop_id):
    """
    获取上游 uid
    """
    if not uid:
        return 0

    row = conn.execute('SELECT * FROM  buyer_relation WHERE uid=%s AND shop_id=%s', (uid, shop_id)).fetchone()

    if row:
        return row['p1_uid']
    return 0


def search(conn, filters, page, per_page, condition=None):
    """

    :param conn:
    :type conn: sqlalchemy.engine.base.Connection
    :param filters:
    :param page:
    :param per_page:
    :param condition:
    :return:
    """
    result = {}

    sql_filter = {}
    if condition is not None:
        sql_filter = dict(sql_filter, **condition)
    if filters is not None:
        sql_filter = dict(sql_filter, **filters)

    where_sql, where_val = make_where(sql_filter)
    sql = 'SELECT * FROM buyer_relation'
    count_sql = 'SELECT count(*) AS c  FROM buyer_relation'
    if where_sql:
        sql += where_sql
        count_sql += where_sql

    sql += ('order by id desc limit %d,%d' % ((page - 1) * per_page, per_page))

    rows = conn.execute(sql, where_val).fetchall()
    count_row = conn.execute(count_sql, where_val).fetchone()
    total = count_row['c']

    pages = helper.get_page_count(count_row['c'], per_page)

    result['items'] = rows
    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result
