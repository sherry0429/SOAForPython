# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class is service center engine, it's will call service one by one
"""
from scheduler import ParamScheduler
from multiprocessing import Process
import time
from template import ServiceProgramTemplate
from template import ServiceParamTemplate
import subprocess


class ServiceEngine(Process):

    def __init__(self, conf):
        super(ServiceEngine, self).__init__()
        self.conf = conf

    def log_thing(self, log_str):
        print log_str

    def run(self):
        scheduler = ParamScheduler(self.conf)
        scheduler.subscribe_service()
        while True:
            msg = scheduler.get_new_service()
            if msg is not None:
                self.log_thing("runner : %s" % str(msg.__dict__))
                service_instance = ServiceProgramTemplate()
                service_instance.set_param_template(msg)
                service_instance.build()
                service_process = ServiceBootstrap(service_instance)
                service_process.start()
            time.sleep(1)


class ServiceBootstrap(Process):

    def __init__(self, service):
        super(ServiceBootstrap, self).__init__()
        self.service = service

    def run(self):
        """
        all output will write to output.file in dir, watcher will check to make sure it's progress
        :return:
        """
        work_path = self.service.param_template.g_work_path
        service_id = self.service.param_template.g_service_id
        service_name = self.service.param_template.s_service_name
        service_args = self.service.param_template.s_service_args
        cmd = 'python %s/%s/%s' % (work_path, service_id, service_name)
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
        except Exception, error_msg:
            print error_msg

