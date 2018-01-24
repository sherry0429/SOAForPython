# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from multiprocessing import Process
from threading import Thread
from scheduler import ParamScheduler
import time
import os


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
            if msg is not None and msg.param_template.o_watcher_enabled is True:
                self.log_thing("watcher : %s" % str(msg.__dict__))
                service_watcher = WatcherThread(msg, self.conf)
                self.services_watcher[msg.param_template.g_service_id] = service_watcher
                service_watcher.start()
            # todo here sleep interval define by param
            time.sleep(1)


class WatcherThread(Thread):

    def __init__(self, service_instance, conf):
        super(WatcherThread, self).__init__()
        self.conf = conf
        self.service_instance = service_instance
        self.interval = self.service_instance.param_template.o_watcher_interal

    def run(self):
        scheduler = ParamScheduler(self.conf)
        self.service_instance.watcher_handler.before_watch_callback()
        service_id = self.service_instance.param_template.g_service_id
        service_name = self.service_instance.param_template.s_service_name
        workpath = self.service_instance.param_template.g_work_path + "/" + self.service_instance.param_template.g_service_id
        list_file = None
        if workpath is not None and os.path.exists(workpath):
            while True:
                list_file = os.listdir(workpath)
                user_signal = self.service_instance.watcher_handler.file_change_callback(len(list_file))
                if user_signal == -1 or scheduler.check_service_state(service_id) is not None:
                    break
                # todo except user signal, when check redis-key [service_id] finished, this loop also break
                time.sleep(self.interval)
        self.service_instance.watcher_handler.after_watch_callback(list_file)
        print 'watcher thread for service %s/%s stopped' % (service_id, service_name)








