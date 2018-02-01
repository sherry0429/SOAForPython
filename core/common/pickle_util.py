# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import pickle


class PickleUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def p_encode(class_instance):
        return pickle.dumps(class_instance)

    @staticmethod
    def p_decode(encode_str):
        return pickle.loads(encode_str)