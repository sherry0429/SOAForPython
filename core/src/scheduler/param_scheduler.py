# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from common import RedisUtil
from common import PickleUtil


class ParamScheduler(object):

    def __init__(self, conf):
        self.redis = RedisUtil(conf['redis']['ip'],
                               conf['redis']['port'],
                               conf['redis']['db'])

    def publish_service(self, value):
        if value.__class__.__name__ == 'ServiceParamTemplate':
            binary_data = self.encode_param(value)
            self.redis.publish('add-service', binary_data)

    def subscribe_service(self):
        self.redis.subscribe('add-service')

    def get_new_service(self):
        msg = self.redis.get_message()
        if msg is not None:
            if msg['data'] != '' and msg['data'] is not None:
                data = self.decode_param(msg['data'])
                if data.__class__.__name__ == 'ServiceParamTemplate':
                    return data
        return None

    def encode_param(self, param):
        return PickleUtil.dumps_param(param)
    
    def decode_param(self, param):
        return PickleUtil.loads_param(param)