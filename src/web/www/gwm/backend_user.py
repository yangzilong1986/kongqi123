# coding:utf-8


from api.helper import update_table_row


def get_info(conn, uid):
    """
    获取后台用户信息
    :param uid:
    :return:
    """
    return conn.execute('SELECT * FROM backend_user WHERE uid=%s', (uid,)).fetchone()


def check_login(conn, username, password):
    """
    登录校验
    """

    return conn.execute('SELECT * FROM backend_user WHERE username=%s AND password=%s LIMIT 1',
                        (username, password)).fetchone()


def edit(conn, uid, info):
    """
    编辑用户信息
    :param uid:
    :param info:
    :return:
    """

    return update_table_row(conn, 'backend_user', {'id': uid}, info)
