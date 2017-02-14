# coding:utf-8
import itertools
import logging

from api import helper

log = logging.getLogger('api')


def get_info(conn, pid):
    """
    商品信息
    {
        "update_time": "2016-08-17 13:51:54",
        "_sa_instance_state": null,
        "product_property_list": [
            {
                "name": "尺寸",
                "value": [
                    "小",
                    "大"
                ]
            },
            {
                "name": "颜色",
                "value": [
                    "蓝",
                    "绿",
                    "红"
                ]
            }
        ],
        "name": "马蓉同款",
        "is_delete": 0,
        "cover_img": "first/78/1471413104",
        "commission_amount": "20.00",
        "price": "100.00",
        "is_recommend": 1,
        "sales": 0,
        "shop_id": 1,
        "create_time": "2016-08-17 13:51:54",
        "inventory": 100,
        "pub_uid": 1,
        "id": 1,
        "product_img_list": [
            "first/78/1471413104"
        ],
        "description": "马蓉同款\n\n马蓉同款\n\n马蓉同款马蓉同款马蓉同款\n\n马蓉同款马蓉同款马蓉同款\n"
    }
    :param conn:
    :param pid:
    :return:
    """

    _product_info = conn.execute('select * from product where id=%d', (pid, )).fetchone()
    if not _product_info:
        return None

    # 获取商品属性列表
    property_list = get_product_property_list(_product_info['id'])
    if property_list:
        _product_info['product_property_list'] = property_list

    # 获取商品图片列表
    img_list = get_product_img_list(_product_info['id'])
    if img_list:
        _product_info['product_img_list'] = [img_item['img_url'] for img_item in img_list]

    # 获取商品封面图片
    cover_img = get_product_cover_img(_product_info['id'])
    if cover_img:
        _product_info['cover_img'] = cover_img.get('img_url')

    return _product_info


def get_info_by_name(conn, name):
    """
    按名取基本信息
    :param conn:
    :param name:
    :return:
    """
    return helper.get_table_one_row(conn, 'product', {'name': name})


def get_list_by_like(conn, shop_id, name):
    """
    按名取基本信息
    :param conn:
    :param shop_id
    :param name:
    :return:
    """
    rows = conn.execute("select * from product where shop_id = %d and `name` like '%" + name + "%'", (shop_id, )).fetchall()

    return helper.to_list(rows)


def add(conn, info):
    """
    新增商品
    :param conn:
    :param info:
    :return:
    """
    product_id = None
    log.info('add product info:%s' % (str(info),))

    if 'product' in info:
        r = helper.insert_table(conn, 'product', info['product'])
        log.info('ret:%s' % (r,))
        product_id = r
        log.info('ret:product_id:%s' % (product_id, ))

    if product_id and 'product_property' in info:
        for item in info['product_property']:
            item['product_id'] = product_id
            helper.insert_table(conn, 'product_property', item)

    if product_id and 'product_img' in info:
        for item in info['product_img']:
            item['product_id'] = product_id
            helper.insert_table(conn, 'product_img', item)

    return product_id


def edit(conn, product_id, info):
    """
    编辑商品
    :param conn:
    :param product_id:
    :param info:
    :return:
    """

    if 'product' not in info:
        return None

    return helper.update_table_row(conn, 'product', {'id': product_id}, info['product'])


def up(conn, product_id):
    """
    商品上架
    :param conn:
    :param product_id:
    """
    return helper.update_table_row(conn, 'product', {'id': product_id}, {'is_delete': 0})


def down(conn, product_id):
    """
    商品下架
    :param conn:
    :param product_id:
    """
    return helper.update_table_row(conn, 'product', {'id': product_id}, {'is_delete': 1})


def search(conn, filters, page, per_page, condition=None):
    """
    搜索
    分页：
        items: 信息列表
        has_next: 如果本页之后还有超过一个分页，则返回True
        has_prev: 如果本页之前还有超过一个分页，则返回True
        next_num: 返回下一页的页码
        prev_num: 返回上一页的页码
    """
    keyword = filters.get('keyword')
    price_min = filters.get('price_min')
    price_max = filters.get('price_max')
    sales_min = filters.get('sales_min')
    sales_max = filters.get('sales_max')

    sql_select = 'SELECT * FROM  product '
    sql_count = 'SELECT count(*) as c FROM  product '
    sql = ''
    sql_val = ()
    result = {}
    if condition:
        sql_where, sql_val = helper.make_where(condition)
        sql += ' and ' + sql_where

    if keyword:
        sql += ' and name like %s'
        sql_val += ('%' + keyword + '%',)
    if price_min:
        sql += ' and price >= %s'
        sql_val += (price_min,)
    if price_max:
        sql += ' and price <= %s'
        sql_val += (price_max,)
    if sales_min:
        sql += ' and price >= %s'
        sql_val += (sales_min,)
    if sales_max:
        sql += ' and price <= %s'
        sql_val += (sales_max,)

    if sql.startswith(' and '):
        sql = sql[len(' and '):]
    if sql:
        sql = 'where ' + sql

    sql_order = ' order by id desc limit %d,%d' % ((page - 1) * per_page, per_page)

    sql_select += sql
    sql_count += sql

    # log.debug('sql:' + sql_select + ' | ' + str(sql_val))
    # log.debug('sql:' + sql_count + ' | ' + str(sql_val))
    rows = helper.to_list(conn.execute(sql_select + sql_order, sql_val).fetchall())
    total = conn.execute(sql_count, sql_val).fetchone()['c']

    pages = helper.get_page_count(total, per_page)

    for row in rows:
        img = get_product_cover_img(conn, row['id'])
        if img:
            row['img_url'] = img.get('img_url')

    result['items'] = rows
    result['total'] = total['c']
    result['pages'] = pages
    result['has_next'] = page < pages
    result['has_prev'] = page > 1
    result['next_num'] = page + 1
    result['prev_num'] = page - 1
    return result


def get_product_property(conn, product_property_id):
    """
    获取商品属性
    :param conn
    :param product_property_id
    """
    return helper.get_table_one_row(conn, 'product_property', {'id': product_property_id})


def get_product_property_list(conn, product_id):
    """
    获取商品属性列表
    [
        {
            "value_list": [
                {
                    "id": 1,
                    "value": "小"
                },
                {
                    "id": 2,
                    "value": "大"
                }
            ],
            "name": "尺寸"
        },
        {
            "value_list": [
                {
                    "id": 3,
                    "value": "蓝"
                },
                {
                    "id": 4,
                    "value": "绿"
                },
                {
                    "id": 5,
                    "value": "红"
                },
                {
                    "id": 39,
                    "value": "中"
                }
            ],
            "name": "颜色"
        }
    ]
    """
    property_list = helper.get_table_rows(conn, 'product_property', {'product_id': product_id})

    result = [({'name': g, 'value_list': [{'id': i['id'], 'value': i['value']} for i in list(k)]}) for g, k in
              itertools.groupby(property_list, lambda x: x['name'])]
    return result


def get_product_img(conn, product_img_id):
    """
    获取商品图片
    """
    return helper.get_table_one_row(conn, 'product_img', {'id': product_img_id})


def get_product_cover_img(conn, product_id):
    """
    获取商品封面图片
    """
    return helper.get_table_one_row(conn, 'product_img', {'product_id': product_id, 'is_cover': 1})


def get_product_img_list(conn, product_id):
    """
    获取商品图片列表
    """
    rows = helper.get_table_rows(conn, 'product_img', {'product_id': product_id})

    return helper.to_list(rows)


def add_product_img(conn, info):
    """
    添加商品图片
    """
    return helper.insert_table(conn, 'product_img', info)


def edit_product_img(conn, product_img_id, info):
    """
    编辑商品图片
    """
    return helper.update_table_row(conn, 'product_img', {'id': product_img_id}, info)


def delete_product_img(conn, product_img_id):
    """
    删除商品图片
    """
    return conn.execute('delete from product_img where `id` = %d' % product_img_id)


def get_list(conn, last_id, limit, condition=None):
    """
    获取商品列表 商品id降序（动态加载）
    :param conn:
    :param last_id: 页面传递过来的的最小id
    :param limit:
    :param condition:
    :return:
    [
        {
            "update_time": "2016-08-11 18:09:41",
            "_sa_instance_state": null,
            "description": "12\n\n2\n\n222\n\n<img src=\"http://ob2dwbbpj.bkt.clouddn.com/first/59/1470909914?imageView2/2/w/600\"><img src=\"http://ob2dwbbpj.bkt.clouddn.com/first/75/1470909914?imageView2/2/w/600\">\n",
            "is_delete": 2,
            "cover_img": "first/85/1470909906",
            "commission_amount": "10.00",
            "price": "1000.00",
            "is_recommend": 0,
            "sales": 0,
            "shop_id": 6,
            "create_time": "2016-08-11 18:08:35",
            "inventory": 445,
            "pub_uid": 14,
            "id": 5,
            "name": "冬笋2"
        },
        {
            "update_time": "2016-08-11 18:12:41",
            "_sa_instance_state": null,
            "product_property_list": [
                {
                    "name": "尺寸",
                    "value": [
                        "小",
                        "大"
                    ]
                },
                {
                    "name": "颜色",
                    "value": [
                        "蓝",
                        "绿",
                        "红"
                    ]
                }
            ],
            "description": "<p>冬笋1</p>\r\n\r\n<p> </p>\r\n\r\n<p> </p>\r\n\r\n<p>冬笋2</p>\r\n\r\n<p><img key=\"first/5/1470903328\" src=\"http://ob2dwbbpj.bkt.clouddn.com/first/5/1470903328?imageView2/2/w/600\" /></p>\r\n\r\n<p><img key=\"first/56/1470903328\" src=\"http://ob2dwbbpj.bkt.clouddn.com/first/56/1470903328?imageView2/2/w/600\" /></p>\r\n\r\n<p> </p>\r\n\r\n<p style=\"text-align: justify;\"> </p>\r\n\r\n<p><img key=\"first/03/1470903425\" src=\"http://ob2dwbbpj.bkt.clouddn.com/first/03/1470903425?imageView2/2/w/600\" /><img key=\"first/29/1470903425\" src=\"http://ob2dwbbpj.bkt.clouddn.com/first/29/1470903425?imageView2/2/w/600\" /><img key=\"first/37/1470903425\" src=\"http://ob2dwbbpj.bkt.clouddn.com/first/37/1470903425?imageView2/2/w/600\" /></p>\r\n",
            "is_delete": 0,
            "cover_img": "first/88/1470903319",
            "commission_amount": "10.00",
            "price": "100.11",
            "is_recommend": 1,
            "sales": 0,
            "shop_id": 6,
            "create_time": "2016-08-11 16:19:22",
            "inventory": 4,
            "pub_uid": 14,
            "id": 4,
            "name": " 10公斤优质鲜嫩冬笋无污染竹园"
        }
    ]

    """
    sql = 'SELECT * FROM  `product` WHERE id < %s' % (last_id,)
    sql_val = ()
    if condition:
        sql_where, sql_val = helper.make_where(condition)
        sql += ' and ' + sql_where
    sql += ' order by id desc limit %d' % (limit,)
    rows = helper.to_list(conn.execute(sql, sql_val).fetchall())

    for row in rows:
        # 获取商品属性列表
        property_list = get_product_property_list(conn, row['id'])
        if property_list:
            row['product_property_list'] = property_list

        # 获取商品封面图片
        cover_img = get_product_cover_img(conn, row['id'])
        if cover_img:
            row['cover_img'] = cover_img.get('img_url')

    return rows


def shop_all_products(conn, shop_id):
    """
    取商铺下所有的商品列表
    :param conn:
    :param shop_id:
    :return:
    """
    rows = helper.get_table_rows(conn, 'product', {'shop_id': shop_id})

    return helper.to_list(rows)


def search_product_title(conn, keywords, limit=10):
    """
    搜索商品标题列表
    """
    rows = conn.execute('select * from product where `name` like %' + keywords + '% order by `id` desc limit ' + str(limit))

    return helper.to_list(rows)


def add_product_property(conn, info):
    """
    添加商品属性
    """
    return helper.insert_table(conn, 'product_property', info)


def edit_product_property(conn, product_property_id, info):
    """
    编辑商品属性
    """
    return helper.update_table_row(conn, 'product_property', {'id': product_property_id}, info)


def delete_product_property(conn, product_property_id):
    """
    删除商品属性
    """
    return conn.execute('delete from product_property where id=%s ', (product_property_id,))


def delete_product_property_by_name(conn, product_id, product_property_name):
    """
    根据商品属性名称删除所有属性值
    """
    return conn.execute('delete from product_property where `product_id`=%s and `name`=%s', (product_id, product_property_name,))


