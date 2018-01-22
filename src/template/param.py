# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>

this file define param file 's rules, what's is 'must', what's is 'optional'

param in GlobalParam Class means it's global param, all service need it.
param in SwitchParam means it's param for template, it's will influence some interval/function, if not set, it will use default.
param in SpecialParam means ServiceInstance's param, template will not use them, but children class can get them.
"""


class ServiceParamTemplate(object):
    """
    do not add any param in this base class, make sure it's clear.
    """
    not_null_attr = [
        'work_path',
        'input_file',
        'output_file',
        'service_path'
    ]

    class GlobalParam(object):
        """
        this class include lots of param all service use
        """
        work_path = None  # service's work path, it's must be an empty path.
        input_file = None  # input file name
        output_file = None  # output file name
        service_path = None  # python scripts path, like jet3d.py

        def __init__(self):
            pass

        @classmethod
        def log_thing(cls, log_str):
            print log_str

    class SwitchParam(object):
        """
        this class include some switch, changed them will change engine's operation about template
        """

        watcher_enabled = True  # whether boot watcher, if not, all callback will not be called.
        watcher_interal = 3

        def __init__(self):
            pass

        @classmethod
        def log_thing(cls, log_str):
            print log_str

    class SelfParam(object):
        """
        this class make every template unique, but if not set, every template instance have a md5 make it different
        also, you can register param on it, and define a dict, it's will transport to service scripts

        for example, you can make a unique prefix, all param have unique prefix will be send to service
        1.you define: s_time, s_step, s_file
        2.register them to this class
        3.call get_param, you will get a param'name set
        4.for i in param_set:
            if "s_" in i:
                exec 'your_set.append(SelfParam.%s)' % i
          and when it's over, 'your_set' is all you need

        also you can call register service param method, return your set,
        and engine will send all this param to service.
        """
        param_set = set()
        service_name = None
        user_id = None
        service_args = dict()

        def __init__(self):
            pass

        @classmethod
        def register_param(cls, param_dict):
            if not isinstance(param_dict, dict):
                cls.log_thing("type error, param is not dict")
                return
            else:
                for (p_k, p_v) in param_dict.items():
                    if not isinstance(p_k, basestring):
                        cls.log_thing('illegal attribute\'s type %s, it is must be string' % str(p_k))
                        continue
                    if isinstance(p_v, basestring):
                        exec 'cls.%s = \'%s\'' % (p_k, p_v)
                    elif isinstance(p_v, list):
                        exec 'cls.%s = list()' % (p_k)
                    elif isinstance(p_v, set):
                        exec 'cls.%s = set()' % (p_k)
                    elif isinstance(p_v, tuple):
                        exec 'cls.%s = tuple()' % (p_k)
                    elif isinstance(p_v, dict):
                        exec 'cls.%s = dict()' % (p_k)
                    exec 'cls.param_set.add(\'%s\')' % (p_k)

        @classmethod
        def get_param(cls):
            return cls.param_set

        @classmethod
        def set_service_param(cls, param_dict):
            if not isinstance(param_dict, dict):
                cls.log_thing("type error, param is not dict")
                return
            for (k, v) in param_dict.items():
                if k in cls.service_args.keys():
                    cls.log_thing('repeat attribute name')
                cls.service_args[k] = v

        @classmethod
        def log_thing(cls, log_str):
            print log_str


if __name__ == '__main__':
    """
    this is example for: 
    1.init template
    2.register para
    3.get param list
    4.set service param
    """
    # 1 init template
    template = ServiceParamTemplate()
    # 2 register para
    a = dict()
    a['a'] = 'b'
    template.SelfParam.register_param(a)
    # 3 get param list (default param and register param)
    print template.SelfParam.get_param()
    # 4 set service param
    template.SelfParam.set_service_param(a)
