# coding:utf-8
"""
baidu 地图 坐标距离计算

"""

import urllib
import json

import requests

import logging

log = logging.getLogger('db')
HTTP_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

_config_gps = {
    'oid': '3041',
    'key': '1601EDEFA68FBC18E7A00038745E8699',
}

from .db import create_conn

conn = create_conn()


# #### 坐标转换 代码开始 ######

def find_cache(point):
    rows = conn.execute('select * from match_cache_gps where baidu_lng=%s and baidu_lat=%s limit 1',
               (point['lng'], point['lat'])).fetchall()

    ret = None
    if len(rows) > 0:
        ret = {'lat': rows[0]['gps_lat'], 'lng': rows[0]['gps_lng']}

    return ret


def save_cache(point, gps_point):

    params = (point['lng'], point['lat'], gps_point['lng'], gps_point['lat'])
    log.debug('params:%s' % (str(params)))
    try:
        if find_cache(point):
            return
        conn.execute('insert into match_cache_gps(baidu_lng,baidu_lat,gps_lng,gps_lat)values(%s,%s,%s,%s) ', params)

    except Exception as e:
        log.exception(e)



def get_gps_with_cache(point_list):
    """
    获取gps 坐标,带缓存
    :param point_list:
    :return:
    """

    new_data = []
    result = [None] * len(point_list)

    result_map = {}
    for i, p in enumerate(point_list):
        cache_data = find_cache(p)
        if cache_data is not None:
            result[i] = cache_data
            log.debug('hit cache:%s' % (str([p, cache_data])))
            continue
        # 位置映射
        result_map[len(new_data)] = i
        new_data.append(p)

    log.debug('result len:%s' % (len(result)))
    if len(new_data):

        for i2 in range(0, len(new_data) + 1, 20):
            gps_result = baidu2gps(new_data[i2:i2 + 20])
            for i, p in enumerate(gps_result):
                src_key = result_map[i2 + i]
                log.debug('save cache:%s' % (str([point_list[src_key], p])))
                save_cache(new_data[i], p)
                log.debug(str(['set ', src_key, p, 'i2:', i2, 'i:', i]))
                result[src_key] = p

    log.info(str(['result:', result]))
    return result


def baidu2gps(point_list):
    """
    每组纬度在前，经度在后。最大20组。分隔符;
http://api.gpsspg.com/convert/coord/?key=1601EDEFA68FBC18E7A00038745E8699&oid=3041&from=0&to=4&latlng=22.9621107600,113.9826665700
http://api.gpsspg.com/convert/coord/?key=1601EDEFA68FBC18E7A00038745E8699&oid=3041&from=0&to=4&latlng=84.21,38.70
http://api.gpsspg.com/convert/coord/?key=1601EDEFA68FBC18E7A00038745E8699&oid=3041&from=0&to=4&latlng=31.233127,121.485885
    :param p: 类似:31.0026777169,108.7051969740
    :return:
    """
    url = 'http://api.gpsspg.com/convert/coord/?'
    params = {
        'oid': _config_gps['oid'],
        'key': _config_gps['key'],
        'from': "2",
        'to': "0",
        # //latlng'': "31.0026777169,108.7051969740",
        'latlng': ';'.join(['%s,%s' % (p['lat'], p['lng']) for p in point_list]),
    }
    url += urllib.urlencode(params)

    s = requests.session()
    s.headers.update(HTTP_HEADER)
    res = s.get(url)
    d = json.loads(res.text)
    # print json.dumps(d, ensure_ascii=False, indent=2)
    if d['status'] != 200:
        raise Exception(d['msg'])
    return d['result']


def test_baidu2gps2():
    p = [{'lat': '31.159351', 'lng': '121.487012'}]
    p2 = baidu2gps(p)
    print 'p(%s)=>p2(%s)' % (p, p2)


def test_baidu2gps_cache():
    p = [{'lat': '31.159351', 'lng': '121.487012'}]
    p2 = get_gps_with_cache(p)
    print 'p(%s)=>p2(%s)' % (p, p2)


def test_get_service_gps_point():


    def str2point(p):
        arr = p.strip().split(',')
        return {'lng': arr[0], 'lat': arr[1]}

    rows = conn.execute("select * from service where coordinate<>'' order by  coordinate limit 90,30")
    points = [str2point(row['coordinate']) for row in rows.fetchall()]
    points2 = get_gps_with_cache(points)
    print 'points2'
    print points2


# #### 坐标转换 end ######


# 百度 坐标距离 求:
# 参考
# 1. http://www.cnblogs.com/MaxIE/p/3914762.html
# 2. http://blog.csdn.net/pleasurelong/article/details/26855049

import math


def max(a, b):
    if a > b:
        return a
    return b


def min(a, c):
    if a > c:
        return c
    return a


def lw(a, b, c):
    #     b != n && (a = Math.max(a, b));
    #     c != n && (a = Math.min(a, c));
    a = max(a, b)
    a = min(a, c)
    return a


def ew(a, b, c):
    while a > c:
        a -= c - b
    while a < b:
        a += c - b
    return a


def oi(a):
    return math.pi * a / 180


def cut_num(num,min_val,max_val):
    if num > max_val:
        return max_val
    elif num < min_val:
        return min_val
    else:
        return num


def Td(a, b, c, d):
    t0 = math.sin(c) * math.sin(d) + math.cos(c) * math.cos(d) * math.cos(b - a)
    t0 = cut_num(t0, -1.0, 1.0)
    t = math.acos(t0)
    return t * 6370996.81
    # return 6370996.81 * math.acos(math.sin(c) * math.sin(d) + math.cos(c) * math.cos(d) * math.cos(b - a))


def Wv(a, b):
    if not a or not b:
        return 0
    a['lng'] = ew(a['lng'], -180, 180)
    a['lat'] = lw(a['lat'], -74, 74)
    b['lng'] = ew(b['lng'], -180, 180)
    b['lat'] = lw(b['lat'], -74, 74)
    return Td(oi(a['lng']), oi(b['lng']), oi(a['lat']), oi(b['lat']))


def get_distance(a, b):
    """
    获取 2点距离
    >>>p1 = {'lng': 121.487012, 'lat': 31.159351}
    >>>p2 = {'lng': 121.485885, 'lat': 31.233127}
    >>>d = get_distance(p1, p2)
    >>>print '计算距离:', d / 1000, 'km'
    >>># 8.2km
    :param a:
    :param b:
    :return:
    """
    c = Wv(a, b)
    return c
