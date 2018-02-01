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

    def lpush(self, key, value):
        self.redis_c.lpush(key, value)

    def rpop(self, key):
        return self.redis_c.rpop(key)

    def get_keys_by_parrten(self, pattern):
        return self.redis_c.keys(pattern)

    def hset(self, key_r, key_v, value):
        self.redis_c.hset(key_r, key_v, value)

    def hget(self, key_r, key_v):
        self.redis_c.hget(key_r, key_v)

    def hgetall(self, key_r):
        self.redis_c.hgetall(key_r)