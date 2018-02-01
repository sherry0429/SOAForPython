# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from src import ServiceParamTemplate
import redis
from message import BaseMessage
from common import PickleUtil


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    msg = BaseMessage()
    param_template = ServiceParamTemplate(work_path='work',
                                          service_path='service_pool/servicea.py',
                                          input_file='a',
                                          output_file='b',
                                          s_service_name='servicea')
    msg.content = param_template
    msg.direction = ['core_engine', 'service_engine']
    msg.msg_id = '1'
    redis = redis.StrictRedis('localhost', '6379', 0)
    redis.lpush('bus', PickleUtil.p_encode(msg))