# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from bus_module import CustomMsgBus
from core_module import CoreEngineModule


if __name__ == '__main__':
    bus_engine = CustomMsgBus('localhost', 6379, 0)
    bus_engine.start_bus()
    core_engine = CoreEngineModule('localhost', 6379, 0, 'simple_core')
    core_engine.start()
    print "standalone system start finished ..."

