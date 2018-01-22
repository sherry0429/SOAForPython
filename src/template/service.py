# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class is service program template, it's include a param template and a egg template
"""
from param import ServiceParamTemplate
import os
import shutil


class ServiceProgramTemplate(object):

    def __init__(self):
        self.param_template = None

    def log_thing(self, log_str):
        print log_str

    def set_param_template(self, param_template):
        if not isinstance(param_template, ServiceParamTemplate):
            self.log_thing('illegal param template class')
            return
        passed = True
        missed_attr = list()
        for i in param_template.not_null_attr:
            if getattr(param_template.GlobalParam, i) is not None:
                continue
            else:
                passed = False
                missed_attr.append(i)
        if not passed:
            raise Exception('you miss some not null attribute, %s is needed' % missed_attr)
        self.param_template = param_template

    def build(self):
        # make working path
        work_path = self.param_template.GlobalParam.work_path
        if os.path.exists(work_path):
            self.log_thing("workpath is existed")
            return
        os.makedirs(work_path)
        # copy exe scripts from egg_template
        service_path = self.param_template.GlobalParam.service_path
        if os.path.exists(service_path):
            shutil.copyfile(service_path, work_path)
        # get input file in param template
        input_file = self.param_template.GlobalParam.input_file
        if "ftp://" in input_file:
            pass
        elif os.path.exists(input_file):
            shutil.copy2(input_file, work_path)
        else:
            # in db, hdfs, or other...
            pass











