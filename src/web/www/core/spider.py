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
    def list_job():
        '''
        /listjobs.json?project=spider
        {"status": "ok",
         "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "spider1"}],
         "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "spider2", "start_time": "2012-09-12 10:14:03.594664"}],
         "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "spider3", "start_time": "2012-09-12 10:14:03.594664", "end_time": "2012-09-12 10:24:03.594664"}]}
        :return:
        '''
        url = SCRAPYD_CONFIG['url'] + '/listjobs.json'
        payload = {
            'project': SCRAPYD_CONFIG['project']
        }
        r = requests.get("http://httpbin.org/get", params=payload)
        data = r.json()

        return data

    @staticmethod
    def schedule_job(project, spider, setting, jobid, **kwargs):
        """
        调度任务
        :param project:
        :param spider:
        :param setting:
        :param jobid:
        :param kwargs:
        :return:
        """
        url = '%s/schedule.json' % api_url
        payload = {
            'project': project,
            'spider': spider,
            'setting': setting or [],
            'jobid': jobid or uuid.uuid1().hex
        }
        payload.update(**kwargs)
        result = requests.post(url, data=payload).json()
        # print json.dumps(result, indent=4, ensure_ascii=False)
        return result

    @staticmethod
    def cancel_job(project, job):
        """
        取消任务
        :param project:
        :param job:
        :return:
        """
        url = '%s/cancel.json' % api_url
        payload = {
            'project': project,
            'job': job
        }
        result = requests.post(url, data=payload).json()
        # print json.dumps(result, indent=4, ensure_ascii=False)
        return result

    @staticmethod
    def list_jobs(project='default'):
        """
        查看任务
        :param project:
        :return:
        """
        url = '%s/listjobs.json' % api_url
        params = {
            'project': project
        }
        result = requests.get(url, params=params).json()
        # print json.dumps(result, indent=4, ensure_ascii=False)
        return result

    @staticmethod
    def check_job(project, job, status='running'):
        """
        检查任务
        :param project:
        :param job:
        :param status:pending/running/finished
        :return:
        """
        job_status = list_jobs(project)
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
        job_status = list_jobs(project_name)
        job_ids_pending = set([x['id'] for x in job_status['pending']])
        job_ids_running = set([x['id'] for x in job_status['running']])
        job_ids = job_ids_pending | job_ids_running
        return [job_id for job_id in job_ids if job_id.startswith(domain) and job_id.endswith(str(task_type))]
