# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from multiprocessing import Process
from threading import Thread
from scheduler import ParamScheduler
import time
import os
from template import ServiceProgramTemplate


class WatcherEngine(Process):

    def __init__(self, conf):
        super(WatcherEngine, self).__init__()
        self.conf = conf
        self.services_watcher = dict()

    def log_thing(self, log_str):
        print log_str

    def run(self):
        scheduler = ParamScheduler(self.conf)
        scheduler.subscribe_service()
        while True:
            msg = scheduler.get_new_service()
            if msg is not None and msg.o_watcher_enabled is True:
                self.log_thing("watcher : %s" % str(msg.__dict__))
                service_instance = ServiceProgramTemplate()
                service_instance.set_param_template(msg)
                service_watcher = WatcherThread(service_instance)
                self.services_watcher[msg.g_service_id] = service_watcher
                service_watcher.start()
            time.sleep(1)


class WatcherThread(Thread):

    def __init__(self, service_instance):
        super(WatcherThread, self).__init__()
        self.service_instance = service_instance
        self.interval = self.service_instance.param_template.o_watcher_interal

    def run(self):
        hander = self.service_instance.param_template.o_watcher_handler
        hander.before_watch_callback()
        build_file_list = set()
        while True:
            workpath = self.service_instance.param_template.g_work_path + "/" + self.service_instance.param_template.g_service_id
            if workpath is not None and os.path.exists(workpath):
                for output_file in os.listdir(workpath):
                    if os.path.isfile(os.path.join(workpath, output_file)):
                        build_file_list.add(output_file)
                        hander.file_change_callback(len(build_file_list))
            time.sleep(self.interval)
        handler.after_watch_callback(build_file_list)








