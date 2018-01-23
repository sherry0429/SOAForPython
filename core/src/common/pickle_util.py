# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import copy_reg
import types
import pickle


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


class PickleUtil(object):

    copy_reg.pickle(types.MethodType, _pickle_method)

    def __init__(self):
        pass

    @classmethod
    def dumps_param(self, param_class):
        return pickle.dumps(param_class)

    @classmethod
    def loads_param(self, binary_param):
        return pickle.loads(binary_param)