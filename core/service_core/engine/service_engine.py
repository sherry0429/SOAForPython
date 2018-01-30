# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class is service center engine, it's will call service one by one
"""
from common import ParamScheduler
from multiprocessing import Process
from threading import Thread
from template import ServiceProgramTemplate
import importlib
import time
import subprocess
import os
from handler import WatcherHandler


class ServiceEngine(Process):

    def __init__(self, conf):
        super(ServiceEngine, self).__init__()
        self.conf = conf
        self.services_watcher = dict()

    def log_thing(self, log_str):
        print log_str

    def run(self):
        scheduler = ParamScheduler(self.conf)
        scheduler.subscribe_service()
        while True:
            msg = scheduler.get_new_service()
            if msg is not None:
                param_data = scheduler.decode_param(msg)
                service_process = ServiceBootstrap(param_data, self.conf)
                service_process.start()
            time.sleep(1)


class ServiceBootstrap(Process):

    def __init__(self, param, conf):
        super(ServiceBootstrap, self).__init__()
        self.param = param
        self.conf = conf
        self.service = None

    def log_thing(self, log_str):
        print log_str

    def rebuild_class(self, develop_class, type):
        base_class = None
        if type == "service":
            base_class = ServiceProgramTemplate()
        elif type == "handler":
            base_class = WatcherHandler()

        for m_callback in dir(base_class):
            if m_callback[0] != "_":
                if hasattr(develop_class, m_callback):
                    develop_value = getattr(develop_class, m_callback)
                    if develop_value is not None:
                        setattr(base_class, m_callback, develop_value)
        return base_class

    def build_service_instance(self, param_template):
        try:
            service_name = param_template.s_service_name
            service_module = importlib.import_module('develop_side.service.servicetest')
            reload(service_module)
            service_class = getattr(service_module, "%sService" % service_name.upper())
            developer_service = service_class()
            service_base = self.rebuild_class(developer_service, "service")

            handler_module = importlib.import_module('develop_side.handler.servicetest_handler')
            reload(handler_module)
            handler_class = getattr(handler_module, '%sHandler' % service_name.upper())
            develop_handler = handler_class()
            handler_base = self.rebuild_class(develop_handler, "handler")

            if service_base and handler_base is not None:
                service_base.set_param_template(param_template)
                service_base.set_watcher_handler(handler_base)
                service_base.build()
                service_base.prepare_input_file()
                return service_base
            else:
                return None
        except Exception, error_msg:
            print error_msg
            return None

    def run(self):
        """
        all output will write to output.file in dir, watcher will check to make sure it's progress
        :return:
        """
        self.service = self.build_service_instance(self.param)
        service_watcher = None
        if self.service is None:
            self.log_thing("service instance is None")
            return
        self.log_thing("runner : %s" % str(self.service.__dict__))
        if self.service.param_template.o_watcher_enabled is True:
            self.log_thing("watcher : %s" % str(self.service.__dict__))
            service_watcher = WatcherThread(self.service, self.conf)
            service_watcher.start()
        scheduler = ParamScheduler(self.conf)
        work_path = self.service.param_template.g_work_path
        service_id = self.service.param_template.g_service_id
        service_path = self.service.param_template.g_service_path
        service_args = self.service.param_template.s_service_args
        cmd = 'python %s' % service_path
        for (k, v) in service_args.items():
            cmd += " %s=\'%s\'" % (k, v)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            output_file = open('%s/%s/output' % (work_path, service_id), 'w+')
            for line in p.stdout.readlines():
                output_file.write(line)
            retval = p.wait()
            output_file.write('\n' + str(retval))
            output_file.close()
            print 'service %s has been finished, waiting watcher thread ...' % service_path
            scheduler.notice_service_finish(service_id, '0')
        except Exception, error_msg:
            print error_msg
        scheduler.notice_service_finish(service_id, '-1')

        if service_watcher is not None:
            while True:
                if not service_watcher.isAlive():
                    break
        print 'service %s has been finished' % service_path


class WatcherThread(Thread):

    def __init__(self, service_instance, conf):
        super(WatcherThread, self).__init__()
        self.conf = conf
        self.service_instance = service_instance
        self.interval = self.service_instance.param_template.o_watcher_interal

    def run(self):
        scheduler = ParamScheduler(self.conf)
        self.service_instance.watcher_handler.before_watch_callback(self.service_instance)
        service_id = self.service_instance.param_template.g_service_id
        service_name = self.service_instance.param_template.s_service_name
        workpath = self.service_instance.param_template.g_work_path + "/" + self.service_instance.param_template.g_service_id
        list_file = None
        if workpath is not None and os.path.exists(workpath):
            while True:
                list_file = os.listdir(workpath)
                user_signal = self.service_instance.watcher_handler.file_change_callback(len(list_file), self.service_instance)
                if user_signal == -1 or scheduler.check_service_state(service_id) is not None:
                    break
                time.sleep(self.interval)
        self.service_instance.watcher_handler.after_watch_callback(list_file, self.service_instance)
        print 'watcher thread for service %s/%s stopped' % (service_id, service_name)