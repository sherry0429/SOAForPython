# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from src import ServiceParamTemplate
import redis
from src.hander import WatcherHandler
from scheduler import ParamScheduler


class CustomHandler(WatcherHandler):

    def __init__(self):
        super(CustomHandler, self).__init__()

    def after_watch_callback(self, file_list):
        # super(CustomHandler, self).after_watch_callback()
        pass

    def before_watch_callback(self):
        """
        hahahaha
        :return:
        """
        # super(CustomHandler, self).before_watch_callback()
        pass

    def file_change_callback(self, file_list):
        # super(CustomHandler, self).file_change_callback()
        print file_list


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    c_handler = CustomHandler()
    param_template = ServiceParamTemplate(work_path='E:/PyProject/SOAForPython/core/test/work',
                                          service_path='E:/PyProject/SOAForPython/core/test/plugin/service_a.py',
                                          input_file='a',
                                          output_file='b',
                                          handler=c_handler)
    redis = redis.StrictRedis('localhost', '6379', 0)
    schduler = ParamScheduler(conf_dict)
    redis.lpush('service-pipe', schduler.encode_param(param_template))