# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class is service center engine, it's will call service one by one
"""
from service import ServiceProgramTemplate
from service_bootstrap import ServiceBootstrap
from redisutil import RedisUtil
from multiprocessing import Process
import time


class ServiceEngine(Process):

    def __init__(self, conf):
        super(ServiceEngine, self).__init__()
        self.conf = conf

    def log_thing(self, log_str):
        print log_str

    def run(self):
        redis = RedisUtil(self.conf['redis']['ip'], self.conf['redis']['port'], self.conf['redis']['db'])
        redis.subscribe_service()
        while True:
            msg = redis.get_new_service()
            if msg is not None:
                print 'runner : ' + str(msg)
                service_process = ServiceBootstrap(msg)
                service_process.start()
            time.sleep(1)