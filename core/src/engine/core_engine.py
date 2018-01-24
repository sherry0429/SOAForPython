# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from service_engine import ServiceEngine
from watcher_engine import WatcherEngine
import time
from scheduler import ParamScheduler
from template import ServiceProgramTemplate


class CoreEngine(object):

    def __init__(self, conf):
        self.scheduler = ParamScheduler(conf)
        self.service_engine = ServiceEngine(conf)
        self.watcher_engine = WatcherEngine(conf)

    def start(self):
        self.service_engine.start()
        print "service engine start ..."
        self.watcher_engine.start()
        print "watcher engine start ..."
        while True:
            service_instance = self.scheduler.redis.redis_c.rpop('service-pipe')
            if service_instance is not None:
                param_data = self.scheduler.decode_param(service_instance)
                service = ServiceProgramTemplate()
                service.set_param_template(param_data)
                service.build()
                self.scheduler.publish_service(service)
            time.sleep(1)
