# coding:utf-8

from config import SCRAPYD_CONFIG


class Spider(object):
    @staticmethod
    def factory():
        if hasattr(Spider, '_obj'):
            return Spider._obj

        obj = Spider()
        Spider._obj = obj

        return obj

    @staticmethod
    def list_job():
        '''
        /listjobs.json?project=spider
        :return:
        '''
        pass

