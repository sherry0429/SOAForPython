# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>

this file define param file 's rules, what's is 'must', what's is 'optional'

param in GlobalParam Class means it's global param, all service need it.
param in SwitchParam means it's param for template, it's will influence some interval/function, if not set, it will use default.
param in SpecialParam means ServiceInstance's param, template will not use them, but children class can get them.
"""
from abc import ABCMeta, abstractmethod
import time
import base64
from hander import WatcherHandler


class ServiceParamTemplate(object):
    """
    do not add any param in this base class, make sure it's clear.
    """

    __metaclass__ = ABCMeta

    not_null_attr = [
        'g_work_path',
        'g_input_file',
        'g_output_file',
        'g_service_path'
    ]

    def __init__(self, work_path, service_path, input_file, output_file, handler, service_id = None):
        # down this include lots of param all service use
        self.g_work_path = work_path  # service's work path, it's must be an empty path.
        self.g_input_file = input_file  # input file name
        self.g_output_file = output_file  # output file name
        self.g_service_path = service_path  # python scripts path, like jet3d.py
        if service_id is not None:
            self.g_service_id = service_id  # service id, if not be set, it's will e a md5 about service_path & time
        else:
            self.g_service_id = self.make_service_id()
        # down this include some switch, changed them will change engine's operation about template
        self.o_watcher_enabled = True  # whether boot watcher, if not, all callback will not be called.
        self.o_watcher_interal = 3
        if handler.__class__.__bases__[0].__name__ == "WatcherHandler":
            self.o_watcher_handler = self.transform_handler(handler)
        else:
            raise Exception('error type about handler %s' % type(handler))
        """
        down this make every template unique, but if not set, every template instance have a md5 make it different
        also, you can register param on it, and define a dict, it's will transport to service scripts,
        
        all you register param will be add prefix 's_', it's means 'special'

        for example, you can make a unique prefix, all param have unique prefix will be send to service
        1.you register: time, step, file (and it will be registed by s_time, s_step...)
        2.call get_param, you will get a param'name set
        4.
          param_template = ServiceParamTemplate()
          ... # register
          param_set = param_template.get_param()
          for i in param_set:
            if "s_" in i:
                exec 'your_dict[i] = \'param_template.%s\' % i'
          and when it's over, 'your_dict' is all you need

        also you can call register service param method, push your dict,
        and engine will send all this param to service.
        """
        self.s_param_set = set()
        self.s_service_name = None
        self.s_user_id = None
        self.s_service_args = dict()

    def register_param(self, param_dict):
        if not isinstance(param_dict, dict):
            self.log_thing("type error, param is not dict")
            return
        else:
            for (p_k, p_v) in param_dict.items():
                if not isinstance(p_k, basestring):
                    self.log_thing('illegal attribute\'s type %s, it is must be string' % str(p_k))
                    continue
                if isinstance(p_v, basestring):
                    exec 'self.s_%s = \'%s\'' % (p_k, p_v)
                elif isinstance(p_v, list):
                    exec 'self.s_%s = list()' % (p_k)
                elif isinstance(p_v, set):
                    exec 'self.s_%s = set()' % (p_k)
                elif isinstance(p_v, tuple):
                    exec 'self.s_%s = tuple()' % (p_k)
                elif isinstance(p_v, dict):
                    exec 'self.s_%s = dict()' % (p_k)
                exec 'self.param_set.add(\'s_%s\')' % (p_k)

    def transform_handler(self, user_handler):
        """
        transform user side class to server side class
        :param user_handler:
        :return:
        """
        watch_handler = WatcherHandler()
        import types
        watch_handler.after_watch_callback = types.MethodType(user_handler.after_watch_callback, watch_handler)
        watch_handler.before_watch_callback = types.MethodType(user_handler.before_watch_callback, watch_handler)
        watch_handler.file_change_callback = types.MethodType(user_handler.file_change_callback, watch_handler)
        # todo here set attr's attribute read successful in core, but callback method read failed
        setattr(watch_handler, 'a', 'b')
        return watch_handler

    def get_param(self):
        return self.s_param_set

    def set_service_param(self, param_dict):
        if not isinstance(param_dict, dict):
            self.log_thing("type error, param is not dict")
            return
        for (k, v) in param_dict.items():
            if k in self.s_service_args.keys():
                self.log_thing('repeat attribute name')
            self.s_service_args[k] = v

    def log_thing(self, log_str):
        print log_str

    def make_service_id(self):
        if self.g_work_path is not None and self.g_service_path is not None:
            base64_origin = str(time.time())
            return base64.encodestring(base64_origin)[-12:-4]
