# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import time
from common import ParamScheduler


class CoreEngine(object):

    def __init__(self, conf):
        self.scheduler = ParamScheduler(conf)

    def start(self):
        while True:
            param_data = self.scheduler.redis.redis_c.rpop('service-pipe')
            if param_data is not None:
                self.scheduler.publish_service(param_data)
            time.sleep(1)
