# coding:utf-8

import requests
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
    def schedule_job(spider, setting, jobid, **kwargs):
        """
        调度任务
        :param project:
        :param spider:
        :param setting:
        :param jobid:
        :param kwargs:
        :return:
        """
        url = SCRAPYD_CONFIG['url'] + '/schedule.json'
        payload = {
            'project': SCRAPYD_CONFIG['project'],
            'spider': spider,
            'setting': setting,
            'jobid': jobid
        }
        payload.update(**kwargs)

        result = False
        try:
            result = requests.post(url, data=payload).json()
            # print json.dumps(result, indent=4, ensure_ascii=False)
            print url, payload, result
        except Exception, e:
            print url, payload, result
            print e.message

        return result

    @staticmethod
    def cancel_job(job):
        """
        取消任务
        :param project:
        :param job:
        :return:
        """
        url = SCRAPYD_CONFIG['url'] + '/cancel.json'
        payload = {
            'project': SCRAPYD_CONFIG['project'],
            'job': job
        }

        result = False
        try:
            result = requests.post(url, data=payload).json()
            # print json.dumps(result, indent=4, ensure_ascii=False)
        except Exception, e:
            print e.message

        return result

    @staticmethod
    def list_spider():
        """
        查看spider
        {"status": "ok", "spiders": ["aqistudy", "tianqihoubao"], "node_name": "wangruideMacBook-Air.local"}
        :param project:
        :return:
        """
        url = SCRAPYD_CONFIG['url'] + '/listspiders.json'
        params = {
            'project': SCRAPYD_CONFIG['project']
        }

        result = False
        try:
            result = requests.get(url, params=params).json()
            # print json.dumps(result, indent=4, ensure_ascii=False)
            # {u'status': u'ok', u'running': [], u'finished': [], u'pending': [], u'node_name': u'wangruider.local'}
        except Exception, e:
            print e.message

        return result

    @staticmethod
    def list_job():
        """
        查看任务
        :param project:
        :return:
        """
        url = SCRAPYD_CONFIG['url'] + '/listjobs.json'
        params = {
            'project': SCRAPYD_CONFIG['project']
        }

        result = False
        try:
            result = requests.get(url, params=params).json()
            # print json.dumps(result, indent=4, ensure_ascii=False)
            # {u'status': u'ok', u'running': [], u'finished': [], u'pending': [], u'node_name': u'wangruider.local'}
        except Exception, e:
            print e.message

        return result

    @staticmethod
    def check_job(job, status='running'):
        """
        检查任务
        :param project:
        :param job:
        :param status:pending/running/finished
        :return:
        """
        job_status = Spider.list_job()
        job_ids = set([x['id'] for x in job_status[status]])
        return job in job_ids

    @staticmethod
    def get_running_task(domain, task_type):
        """
        获取运行中的任务列表
        :param domain:
        :param task_type:
        :return:
        """
        job_status = Spider.list_job()
        job_ids_pending = set([x['id'] for x in job_status['pending']])
        job_ids_running = set([x['id'] for x in job_status['running']])
        job_ids = job_ids_pending | job_ids_running
        return [job_id for job_id in job_ids if job_id.startswith(domain) and job_id.endswith(str(task_type))]
