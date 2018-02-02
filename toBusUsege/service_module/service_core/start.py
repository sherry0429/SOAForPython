# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from engine import ServiceEngineModule


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    s_engine = ServiceEngineModule('localhost', 6379, 0, 'service_core')
    s_engine.start()
    print "Service Engine Start ..."
