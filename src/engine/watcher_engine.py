# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from multiprocessing import Process
from service import ServiceProgramTemplate
from threading import Thread
from redisutil import RedisUtil
import time
import os


class WatcherEngine(Process):

    def __init__(self, conf):
        super(WatcherEngine, self).__init__()
        self.conf = conf
        self.services_watcher = dict()

    def run(self):
        redis = RedisUtil(self.conf['redis']['ip'], self.conf['redis']['port'], self.conf['redis']['db'])
        redis.subscribe_service()
        while True:
            msg = redis.get_new_service()
            if msg is not None:
                print 'watcher : ' + str(msg)
                service_watcher = WatcherThread(msg)
                self.services_watcher[time.asctime()] = service_watcher
                service_watcher.start()
            time.sleep(1)


class WatcherThread(Thread):

    def __init__(self, service_instance):
        super(WatcherThread, self).__init__()
        self.service_instance = service_instance
        self.interval = self.service_instance.param_template.SwitchParam.watcher_interal

    def run(self):
        while True:
            workpath = self.service_instance.param_template.GlobalParam.work_path
            if workpath is not None:
                for output_file_path in os.listdir(workpath):
                    if os.path.isfile(os.path.join(workpath, output_file_path)):
                        print output_file_path
                time.sleep(self.interval)



