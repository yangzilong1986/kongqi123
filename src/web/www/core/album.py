# coding:utf-8


from api import helper


def get_info(conn, album_id):
    """
    获取相片信息
    :param album_id:
    :return:
    """
    return conn.execute('SELECT * FROM album WHERE id=%s', (album_id,)).fetchone()


def album_get_list(conn, endorse_id):
    return conn.execute('SELECT * FROM  album WHERE endorse_id=%s ORDER BY id ', (endorse_id,)).fetchall()


def delete(conn, album_id):
    """
    删除相片信息
    :param album_id:
    :return:
    """
    conn.execute('DELETE FROM album WHERE id=%s LIMIT 1', (album_id,))


def add(conn, info):
    """
    添加相片信息
    :param info:
    :return:
    """
    return helper.insert_table(conn, 'album', info)
