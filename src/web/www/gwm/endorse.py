# coding:utf-8

from api import helper
from api.biz.core import album
from api.biz.core import buyer
from api.biz.core import product
from api.biz.core import shop
from api.helper import get_table_rows, get_table_count, make_where, to_list, update_table_row, insert_table, \
    get_table_one_row
from tools.id_encode import encode_id


def get_info(conn, endorse_id):
    """
    获取代言信息
    :param conn
    :param endorse_id
    :return:
    """
    return get_table_one_row(conn, 'endorse', {'id': endorse_id})


def get_list(conn, condition):
    """
    获取代言列表信息
    :param conn
    :param condition:
    :return:
    """
    return get_table_rows(conn, 'endorse', condition)


def get_count(conn, condition):
    """
    获取代言统计
    :param conn
    :param condition:
    :return:
    """
    return get_table_count(conn, 'endorse', condition)


def list(conn, last_id, limit, condition=None):
    """
    取代言下拉列表
    :param conn
    :param last_id:
    :param limit:
    :param condition:
    :return:
    """

    sql = 'SELECT * FROM endorse WHERE id < %s'
    params = [last_id]
    if condition:
        sql_and, sql_val = make_where(condition)
        sql += 'and ' + sql_and
        params += sql_val

    sql += ' order by id desc limit %s' % limit

    rows = to_list(conn.execute(sql, params).fetchall())

    result = []
    for row in rows:
        endorse = row
        # id变换
        _id = row['id']
        row['id'] = encode_id(_id)
        row['_id'] = _id

        row['_shop_id'] = row['shop_id']
        row['shop_id'] = encode_id(row['shop_id'])

        row['_product_id'] = row['product_id']
        if row['product_id'] > 0:
            row['product_id'] = encode_id(row['product_id'])

        # 获取代言图片

        album_info = album.album_get_list(conn, row[_id])
        album_images = []
        if album_info:
            for url in album_info:
                album_images.append(url['url'])
            endorse['album'] = album_images
        else:
            shop_info = shop.get_shop_info_by_shop_id(conn, row['_shop_id'])
            if shop_info:
                shop_images = shop_info['ad_img'].split(',')
                for ad_img in shop_images:
                    album_images.append(ad_img)
                endorse['album'] = album_images

        # 获取商品信息
        if row['_product_id'] > 0:
            product_info = product.get_info(conn, row['_product_id'])
            if product_info:
                product_info['_id'] = product_info['id']
                product_info['id'] = encode_id(product_info['id'])
                endorse['product'] = product_info

        # 获取用户信息
        buyer_info = buyer.get_info_by_uid(conn, row['uid'])
        if buyer_info:
            endorse['buyer'] = buyer_info

        result.append(endorse)

    return result


def search(conn, filters, page, per_page, condition=None):
    result = {}
    name = filters.get('name')

    sql = 'select * from endorse '
    where = ''
    if condition:
        sql_and, sql_val = make_where(condition)
        where += 'and ' + sql_and

    if name:
        where += 'and product_name like "%' + name + '%"'

    if where:
        where = 'where ' + where
    sql += 'order by id desc limit %d,%d' % ((page - 1) * per_page, per_page)
    rows = to_list(conn.execute(sql).fetchall())

    total = conn.execute('select count(*) c from endorse ' + where).fetchone()

    pages = helper.get_page_count(total['c'], per_page)

    items = []
    for row in rows:
        endorse = row.__dict__ if row else None
        if endorse:
            # id变换
            _id = row.id
            row.id = encode_id(_id)
            row._id = _id

            row._shop_id = row.shop_id
            row.shop_id = encode_id(row.shop_id)

            row._product_id = row.product_id
            if row.product_id > 0:
                row.product_id = encode_id(row.product_id)

            # 商铺信息
            shop_info = shop.get_shop_info_by_shop_id(conn, row['_shop_id'])
            if shop_info:
                endorse['shop_info'] = shop_info

            # 获取代言图片
            album_info = album.album_get_list(conn, row['_id'])
            album_images = []
            if album_info:
                for url in album_info:
                    album_images.append(url['url'])
                endorse['album'] = album_images
            else:
                if shop_info:
                    shop_images = shop_info['ad_img'].split(',')
                    for ad_img in shop_images:
                        album_images.append(ad_img)
                    endorse['album'] = album_images

            # 获取商品信息
            if row['_product_id'] > 0:
                product_info = product.get_info(conn, row['_product_id'])
                if product_info:
                    product_info['_id'] = product_info['id']
                    product_info['id'] = encode_id(product_info['id'])
                    endorse['product'] = product_info

            # 获取用户信息
            buyer_info = buyer.get_info_by_uid(conn, row['uid'])
            if buyer_info:
                endorse['buyer'] = buyer_info

            items.append(endorse)

    result['items'] = items
    result['total'] = total['c']
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1

    return result


def edit(conn, endorse_id, info):
    """
    修改代言信息
    :param conn
    :param endorse_id:
    :param info:
    :return:
    """
    return update_table_row(conn, 'endorse', {'id': endorse_id}, info)


def add(conn, info):
    """
    添加代言信息
    :param conn
    :param info:
    :return:
    """
    return insert_table(conn, 'endorse', info)
