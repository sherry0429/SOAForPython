# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class define list callbacks, use these callback can:

1.do something before watch start (maybe service has been started)
2.do something when service running (receive list file on workpath)
3.do something before watch stop (a watch stop when handler return -1 or service is stopped
"""
from common import RedisUtil
from common import PickleUtil
from template import ServiceProgramTemplate


class ParamScheduler(object):

    def __init__(self, conf):
        self.redis = RedisUtil(conf['redis']['ip'],
                               conf['redis']['port'],
                               conf['redis']['db'])

    def publish_service(self, value):
        if isinstance(value, ServiceProgramTemplate):
            binary_data = self.encode_param(value)
            self.redis.publish('add-service', binary_data)

    def subscribe_service(self):
        self.redis.subscribe('add-service')

    def get_new_service(self):
        msg = self.redis.get_message()
        if msg is not None:
            if msg['data'] != '' and msg['data'] is not None:
                data = self.decode_param(msg['data'])
                if isinstance(data, ServiceProgramTemplate):
                    return data
        return None

    def notice_service_finish(self, service_id, code):
        self.redis.redis_c.hset('services', service_id, code)

    def check_service_state(self, service_id):
        return self.redis.redis_c.hget('services', service_id)

    def encode_param(self, param):
        return PickleUtil.dumps_param(param)
    
    def decode_param(self, param):
        return PickleUtil.loads_param(param)