# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""

from service_core import ServiceEngine
from core_engine import CoreEngine
from bus import MsgBus


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    try:
        bus = MsgBus(conf_dict)
        core = CoreEngine(conf_dict)
        service_core = ServiceEngine(conf_dict)
        bus.start()
        core.start()
        service_core.start()
    except Exception, error_msg:
        print error_msg
    print "start all"