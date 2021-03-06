# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from engine import CoreEngineModule


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    try:
        print "Core Engine Start ..."
        engine = CoreEngineModule(conf_dict)
        engine.start()
    except Exception, error_msg:
        print error_msg
        print "Core Engine Start Failed"
