# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from service_engine import ServiceEngine
from watcher_engine import WatcherEngine
import time
from scheduler import ParamScheduler
from template import ServiceProgramTemplate
import importlib


class CoreEngine(object):

    handler_module_name = 'handler'
    service_module_name = 'service'

    def __init__(self, conf):
        self.scheduler = ParamScheduler(conf)
        self.service_engine = ServiceEngine(conf)
        self.watcher_engine = WatcherEngine(conf)

    def build_service_instance(self, param_template):
        service_name = param_template.s_service_name
        service_base = ServiceProgramTemplate()
        try:
            # todo reload services / handlers dynamic
            """
            for dynamic, all services / watcher callback call in services engine
            merge service_engine and watcher_engine
            core engine only put param template send to watcher engine
            """

            service_module = importlib.import_module('service.servicetest')
            # reload(service_module)
            service_class = getattr(service_module, "%sService" % service_name.upper())
            service = service_class()
            service_base.prepare_input_file = service.prepare_input_file

            handler_module = importlib.import_module('handler.servicetest_handler')
            # reload(handler_module)
            handler_class = getattr(handler_module, '%sHandler' % service_name.upper())
            handler = handler_class()
            handler.after_watch_callback('', '')
            service_base.set_param_template(param_template)
            service_base.set_watcher_handler(handler)

            service_base.build()
            service_base.prepare_input_file()
        except Exception, error_msg:
            print error_msg
        return service_base

    def start(self):
        self.service_engine.start()
        print "service engine start ..."
        self.watcher_engine.start()
        print "watcher engine start ..."
        while True:
            service_instance = self.scheduler.redis.redis_c.rpop('service-pipe')
            if service_instance is not None:
                param_data = self.scheduler.decode_param(service_instance)
                service = self.build_service_instance(param_data)
                self.scheduler.publish_service(service)
            time.sleep(1)
