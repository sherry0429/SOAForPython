# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import redis
import pickle
from toBus import BaseMessage
from service_module import ServiceParamTemplate

if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    msg = BaseMessage()
    param_template = ServiceParamTemplate(work_path='work',
                                          service_path='service_pool/servicetest.py',
                                          input_file='a',
                                          output_file='b',
                                          s_service_name='servicetest')
    msg.content = param_template
    msg.direction = ['simple_core', 'service_core']
    msg.msg_id = '1'
    redis = redis.StrictRedis('localhost', '6379', 0)
    redis.lpush('bus', pickle.dumps(msg))