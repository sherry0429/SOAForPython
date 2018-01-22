# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import redis
import pickle
from service import ServiceProgramTemplate


class RedisUtil(object):

    def __init__(self, ip, port, db=0):
        self.redis_c = redis.StrictRedis(ip ,port, db)
        self.redis_p = self.redis_c.pubsub(ignore_subscribe_messages=True)

    def publish_service(self, value):
        if isinstance(value, ServiceProgramTemplate):
            binary_data = pickle.dumps(value)
            self.redis_c.publish('add-service', binary_data)

    def subscribe_service(self):
        self.redis_p.subscribe('add-service')

    def get_new_service(self):
        msg = self.redis_p.get_message()
        if msg is not None:
            if msg['data'] != '' and msg['data'] is not None:
                data = pickle.loads(msg['data'])
                if isinstance(data, ServiceProgramTemplate):
                    return data
        return None