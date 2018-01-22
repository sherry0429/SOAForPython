# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class get param and start service use subprocess
"""
from multiprocessing import Process
from service import ServiceProgramTemplate
from param import ServiceParamTemplate
import subprocess


class ServiceBootstrap(Process):

    def __init__(self, service):
        super(ServiceBootstrap, self).__init__()
        if not isinstance(service, ServiceProgramTemplate):
            return
        if not isinstance(service.param_template, ServiceParamTemplate):
            return
        self.service_path = service.param_template.GlobalParam.service_path
        self.service_args = service.param_template.SelfParam.service_args
        self.cmd = 'python %s' % self.service_path
        for (k, v) in self.service_args.items():
            self.cmd += " %s=\'%s\'" % (k, v)

    def run(self):
        """
        all output will write to output.file in dir, watcher will check to make sure it's progress
        :return:
        """
        p = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_file = None
        try:
            output_file = open('ouput', 'w')
            for line in p.stdout.readlines():
                output_file.write(line)
            retval = p.wait()
            output_file.write('\n' + str(retval))
        except Exception:
            raise Exception
        finally:
            output_file.close()




