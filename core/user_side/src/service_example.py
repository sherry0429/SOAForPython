# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from src import ServiceParamTemplate
import redis
from common import ParamScheduler


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    param_template = ServiceParamTemplate(work_path='work',
                                          service_path='servicepool/servicetest.py',
                                          input_file='a',
                                          output_file='b',
                                          s_service_name='servicetest')
    redis = redis.StrictRedis('localhost', '6379', 0)
    schduler = ParamScheduler(conf_dict)
    redis.lpush('service-pipe', schduler.encode_param(param_template))