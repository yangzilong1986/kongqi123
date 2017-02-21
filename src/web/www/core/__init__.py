# coding:utf-8

from hashlib import md5


def generate_md5(fp):
    if isinstance(fp, unicode):
        fp = fp.encode('utf-8')

    m = md5()
    m.update(fp)
    return m.hexdigest()
