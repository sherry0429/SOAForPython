# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this base class define a lot's of base way to send msg to bus, or receive msg from bus
"""
# ---------------------------- core side
from pickle_util import PickleUtil
from threading import Thread
import time


class MsgSenderToBus(Thread):

    def __init__(self, redis, module_name, send_queue):
        super(MsgSenderToBus, self).__init__()
        self.module_name = module_name
        self.send_queue = send_queue
        self.redis = redis

    def run(self):
        while True:
            send_msg = self.send_queue.get()
            try:
                send_content = PickleUtil.p_encode(send_msg)
                self.redis.lpush('bus', send_content)
            except Exception, error_msg:
                print error_msg


class MsgReceiverFromBus(Thread):

    def __init__(self, redis, module_name, recv_queue):
        super(MsgReceiverFromBus, self).__init__()
        self.module_name = module_name
        self.recv_queue = recv_queue
        self.redis = redis

    def run(self):
        while True:
            try:
                recv_msg = self.redis.rpop('bus-%s' % self.module_name.lower())
                if recv_msg is not None:
                    recv_content = PickleUtil().p_decode(recv_msg)
                    self.recv_queue.put(recv_content)
            except Exception, error_msg:
                print error_msg
            time.sleep(1)
