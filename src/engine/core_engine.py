# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from service_engine import ServiceEngine
from watcher_engine import WatcherEngine
from redisutil import RedisUtil
import time
import pickle


class CoreEngine(object):

    def __init__(self, conf):
        self.redis = RedisUtil(conf['redis']['ip'], conf['redis']['port'], conf['redis']['db'])
        self.service_engine = ServiceEngine(conf)
        self.watcher_engine = WatcherEngine(conf)

    def start(self):
        self.service_engine.start()
        print "service engine start ..."
        self.watcher_engine.start()
        print "watcher engine start ..."
        while True:
            service_instance = self.redis.redis_c.rpop('service-pipe')
            if service_instance is not None:
                binary_data = pickle.loads(service_instance)
                self.redis.publish_service(binary_data)
            time.sleep(1)


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    engine = CoreEngine(conf_dict)
    engine.start()
