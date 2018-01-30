# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class is service program template, it's include a param template and a egg template
"""
import os
import shutil


class ServiceProgramTemplate(object):

    def __init__(self):
        self.param_template = None
        self.watcher_handler = None

    def log_thing(self, log_str):
        print log_str

    def set_param_template(self, param_template):
        if not param_template.__class__.__name__ == 'ServiceParamTemplate':
            self.log_thing('illegal param template class')
            return
        passed = True
        missed_attr = list()
        for i in param_template.not_null_attr:
            must_attr = getattr(param_template, i)
            if must_attr is not None and must_attr != '':
                continue
            else:
                passed = False
                missed_attr.append(i)
        if not passed:
            raise Exception('you miss some not null attribute, %s is needed' % missed_attr)
        self.param_template = param_template

    def build(self):
        # make working path
        work_path = self.param_template.g_work_path + "/" + self.param_template.g_service_id
        if os.path.exists(work_path):
            self.log_thing("workpath is existed")
            return
        try:
            os.makedirs(work_path)
        except Exception, error_msg:
            self.log_thing(error_msg)
            return
        # copy exe scripts from egg_template
        service_path = self.param_template.g_service_path
        if os.path.exists(service_path):
            shutil.copy(service_path, work_path)
            service_name = service_path.split("/")[-1]
            if self.param_template.s_service_name is None:
                self.param_template.s_service_name = service_name
            self.param_template.g_service_path = "%s/%s.py" % (work_path, self.param_template.s_service_name)
        else:
            return

    def set_watcher_handler(self, handler):
        self.watcher_handler = handler

    def prepare_input_file(self):
        # todo add base operation about this
        pass
        # get input file in param template
        # input_file = self.param_template.g_input_file
        # if "ftp://" in input_file:
        #     pass
        # elif os.path.exists(input_file):
        #     shutil.copy2(input_file, work_path)
        # else:
        #     # in db, hdfs, or other...
        #     pass







