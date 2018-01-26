# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class is service center engine, it's will call service one by one
"""
from scheduler import ParamScheduler
from multiprocessing import Process
import time
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
                service_process = ServiceBootstrap(msg, self.conf)
                service_process.start()
            time.sleep(1)


class ServiceBootstrap(Process):

    def __init__(self, service, conf):
        super(ServiceBootstrap, self).__init__()
        self.service = service
        self.conf = conf

    def run(self):
        """
        all output will write to output.file in dir, watcher will check to make sure it's progress
        :return:
        """
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
            print 'service %s has been finished, exit code %s' % (service_path,
                                                                  str(retval))
            scheduler.notice_service_finish(service_id, '0')
        except Exception, error_msg:
            print error_msg
        scheduler.notice_service_finish(service_id, '-1')


