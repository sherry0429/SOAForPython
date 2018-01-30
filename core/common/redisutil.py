# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import redis


class RedisUtil(object):

    def __init__(self, ip, port, db=0):
        self.redis_c = redis.StrictRedis(ip ,port, db)
        self.redis_p = self.redis_c.pubsub(ignore_subscribe_messages=True)

    def publish(self, channel, data):
        self.redis_c.publish(channel, data)

    def subscribe(self, channel):
        self.redis_p.subscribe(channel)

    def get_message(self):
        return self.redis_p.get_message()