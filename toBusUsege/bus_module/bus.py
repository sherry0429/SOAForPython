# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from toBus import MsgBus


class CustomMsgBus(MsgBus):

    access_modules = set()

    def __init__(self, redis_ip, redis_port, redis_db):
        super(CustomMsgBus, self).__init__(redis_ip, redis_port, redis_db)

    def start_bus(self):
        self.start()

    def msg_recv_callback(self, msg):
        print msg

    def msg_send_callback(self, msg):
        print msg


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    try:
        print "Msg Bus Start ..."
        engine = CustomMsgBus(conf_dict)
        engine.start()
    except Exception, error_msg:
        print error_msg
        print "Msg Bus Start Failed"
