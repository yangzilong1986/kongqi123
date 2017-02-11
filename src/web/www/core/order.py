# coding:utf-8

import json
import logging
from math import ceil

from api import helper
from api.biz.core import product
from api.biz.core.buyer_relation import build_relation
from api.biz.core.wallet import do_commission

log = logging.getLogger('api')


def update_pay_info(conn, order_code, pay_status, pay_info):
    """
    通过订单编号修改订单
    :param conn:
    :param order_code:
    :param pay_status:
    :param pay_info:
    :return:
    """

    params = (pay_status, json.dumps(pay_info), order_code)
    conn.execute('UPDATE `order` SET pay_status=%s ,pay_info=%s ,update_time = now() WHERE order_code = %s LIMIT 1',
                 params)


def get_info(conn, order_id):
    """
    获取订单
    """
    # 获取订单基本信息
    order = helper.get_table_one_row(conn, 'order', {'id': order_id})
    if order:
        # 获取订单详情
        order_items = helper.get_table_rows(conn, 'order_item', {'order_id': order_id})
        for order_item in order_items:
            order_item['product_property'] = json.loads(order_item['product_property'])
        return {'order': order, 'order_items': order_items}
    return None


def get_info_by_code(conn, order_code):
    """
    通过订单编号获取订单信息
    :param conn:
    :param order_code:
    :return:
    """
    order = helper.get_table_one_row(conn, 'order', {'order_code': order_code})
    if order:
        # 获取订单详情
        order_items = helper.get_table_rows(conn, 'order_item', {'order_id': order['id']})
        for order_item in order_items:
            order_item['product_property'] = json.loads(order_item['product_property'])
        return {'order': order, 'order_items': order_items}
    return None


def add(conn, info):
    """
    创建订单
    :param conn:
    :param info:
    :return:
    """
    order_info = info['order']
    order_items = info['order_items']

    shop_info = helper.get_table_one_row(conn, 'shop', {'id': order_info['shop_id']})
    if shop_info is None:
        return
    order_info['shop_uid'] = shop_info['uid']

    order_id = helper.insert_table(conn, 'order', order_info)
    for item in order_items:
        item['order_id'] = order_id
        helper.insert_table(conn, 'order_item', item)
    return order_id


def edit(conn, order_id, info):
    """
    修改订单
    :param conn:
    :param order_id:
    :param info:
    :return:
    """
    return helper.update_table_row(conn, 'order', {'id': order_id}, info)


def delivery(conn, order_id, info):
    """
    发货
    """
    # 添加发货信息
    helper.insert_table(conn, 'order_express', info)
    # 更新订单发货状态
    helper.update_table_row(conn, 'order_express', {'order_id': order_id}, {'goods_status': 1})
    return True


def search(conn, filters, page, per_page, condition=None):
    """
    搜索
    条件：
        filters = {
            'shop_id': '',
            'order_code': '',
            'rec_name': '',
            'rec_phone': '',
            'product_name': '',
        }
    分页：
        items: 信息列表
        has_next: 如果本页之后还有超过一个分页，则返回True
        has_prev: 如果本页之前还有超过一个分页，则返回True
        next_num: 返回下一页的页码
        prev_num: 返回上一页的页码
    items 大体结构：
    items = [
        {
            'order_id': '',
            'order': '',
            'order_items': [
                {
                    'product_id': '',
                    'product_property': [],
                }
            ]
        }
    ]
    """
    buy_uid = filters.get('buy_uid')
    shop_id = filters.get('shop_id')
    order_code = filters.get('order_code')
    rec_name = filters.get('rec_name')
    rec_phone = filters.get('rec_phone')
    product_name = filters.get('product_name')

    sql_select = 'SELECT * FROM `order` LEFT JOIN order_item ON `order`.id = order_item.order_id WHERE 1=1'
    sql_count = 'SELECT count(*) AS c FROM `order` LEFT JOIN order_item ON `order`.id = order_item.order_id WHERE 1=1'
    sql = ''
    sql_val = ()
    result = {}

    if condition:
        sql_where, sql_val = helper.make_where(condition)
        sql += ' and ' + sql_where

    if buy_uid:
        sql += ' and `order`.buy_uid = %s' % (buy_uid,)
    if shop_id:
        sql += ' and `order`.shop_id = %s' % (shop_id,)
    if order_code:
        sql += ' and `order`.order_code = %s' % (order_code,)
    if rec_name:
        sql += ' and `order`.rec_name = %s' % (rec_name,)
    if rec_phone:
        sql += ' and `order`.rec_phone = %s' % (rec_phone,)
    if product_name:
        sql += ' and order_item.product_name like \'%%s%\'' % (product_name,)
    sql += ' order by `order`.id desc limit %d,%d' % ((page - 1) * per_page, per_page)

    sql_select += sql
    sql_count += sql

    rows = helper.to_list(conn.execute(sql_select, sql_val).fetchall())
    total = conn.execute(sql_select, sql_val).fetchone()['c']

    if per_page == 0:
        pages = 0
    else:
        pages = int(ceil(total / float(per_page)))

    result['items'] = []
    for row in rows:
        # 获取订单详情
        order_items = helper.get_table_rows(conn, 'order_item', {'order_id': row['id']})
        for order_item in order_items:
            order_item['product_property'] = json.loads(order_item['product_property'])

            # 获取商品封面图片
            cover_img = product.get_product_cover_img(conn, order_item['product_id'])
            if cover_img:
                order_item['cover_img'] = cover_img.get('img_url')
        result['items'].append({'order': row, 'order_items': order_items})

    result['total'] = total
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result


def get_delivery_info(conn, order_id):
    """
    获取发货信息
    :param conn:
    :param order_id:
    :return:
    """
    return helper.get_table_one_row(conn, 'order_express', {'order_id': order_id})


def edit_delivery_info(conn, order_id, info):
    """
    编辑发货信息
    :param conn:
    :param order_id:
    :param info:
    :return:
    """
    helper.update_table_row(conn, 'order_express', {'order_id': order_id}, info)
    # 修改订单发货状态
    goods_status = info.get('goods_status')
    helper.update_table_row(conn, 'order', {'id': order_id}, {'goods_status': goods_status})
    return True


def get_list(conn, last_id, limit, condition=None):
    """
    获取订单列表 订单id降序（动态加载）
    :param conn:
    :param last_id: 页面传递过来的的最小id
    :param limit:
    :param condition:
    :return:
    """
    if not (last_id or limit):
        return []
    sql = 'SELECT * FROM  `order`'
    if last_id:
        sql += ' WHERE id < %s' % (last_id,)

    sql_val = ()
    if condition:
        sql_where, sql_val = helper.make_where(condition)
        sql += ' and ' + sql_where
    sql += ' order by id desc limit %d' % (limit,)
    rows = helper.to_list(conn.execute(sql, sql_val).fetchall())

    result = []
    for row in rows:
        # 获取订单详情
        order_items = helper.get_table_rows(conn, 'order_item', {'order_id': row['id']})

        for order_item in order_items:
            order_item['product_property'] = json.loads(order_item['product_property'])
        result.append({'order': row, 'order_items': order_items})
    return result


def pay_success(conn, order_code, pay_res_dict=None):
    """
    支付成功之后的处理
        1、保存支付信息
        2、修改支付状态
        3、代言分成
    :param conn:
    :param order_code:
    :param pay_res_dict:
    :return:
    """
    s = conn.begin()
    try:
        order_info = conn.execute('SELECT * FROM `order` WHERE order_code=%s LIMIT 1', (order_code,)).fetchone()
        if order_info is None:
            log.error('order_code:%s, order info is None' % (order_code,))
            return False
        if order_info['pay_status'] == 1:
            log.error('order_code:%s, order info,pay_status  is ok' % (order_code,))
            return False
        # 更新订单信息（支付）,订单状态
        update_pay_info(conn, order_code, 1, pay_res_dict)
        # 建立上下游关系，订单分成
        build_relation(conn, order_code)
        # 执行佣金分成
        do_commission(conn, order_code)
        s.commit()
        return True
    except Exception as e:
        s.rollback()
        raise e


def pay_error(conn, order_code, pay_res_info=None):
    """
    支付失败之后的处理
        1、保存支付信息
        2、修改支付状态
    :param conn:
    :param order_code:
    :param pay_res_info:
    :return:
    """
    return update_pay_info(conn, order_code, 2, pay_res_info)


def is_customer(conn, uid, shop_id):
    """
    判断用户是否是商家的客户
    """
    result = helper.count_table(conn, 'order', {'buy_uid': uid, 'shop_id': shop_id, 'pay_status': 1})
    return bool(result)


def is_bought(conn, uid, product_id):
    """
    判断用户是否买过此商品
    """
    sql_count = 'SELECT count(*) AS c FROM `order` LEFT JOIN order_item ON `order`.id = order_item.order_id WHERE `order`.buy_uid = %s AND order_item.product_id = %s AND `order`.pay_status = %s'
    result = conn.execute(sql_count, (uid, product_id, 1)).fetchone()['c']
    return bool(result)


def get_count(conn, order_condition=None, items_condition=None):
    """
    统计订单计数
    """

    where_sql1, where_params1 = helper.make_where_with_table('order', order_condition)
    where_sql2, where_params2 = helper.make_where_with_table('items', items_condition)
    params = []
    sql = 'SELECT count(*) AS c FROM `order` , order_item WHERE `order`.id = order_item.order_id '
    if where_sql1:
        sql += where_sql1
        params += where_params1
    if where_sql2:
        sql += where_sql2
        params += where_params2
    row = conn.execute(sql, params).fetchone()
    return row['c']
