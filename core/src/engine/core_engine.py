# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import time
from common import RedisUtil
from common import MsgSenderToBus, MsgReceiverFromBus
from Queue import Queue
from threading import Thread


class CoreEngine(object):

    def __init__(self, conf):
        self.redis = RedisUtil(conf['redis']['ip'],
                               conf['redis']['port'],
                               conf['redis']['db'])
        self.module_name = "core_engine"
        self.send_queue = Queue()
        self.recv_queue = Queue()
        self.sender_th = MsgSenderToBus(self.redis, self.module_name, self.send_queue)
        self.receiver_th = MsgReceiverFromBus(self.redis, self.module_name, self.recv_queue)
        self.sender_th.start()
        self.receiver_th.start()

    def start(self):
        core_controller = RecvMsgController(self.recv_queue, self.send_queue)
        core_controller.start()


class RecvMsgController(Thread):

    def __init__(self, recv_queue, send_queue):
        super(RecvMsgController, self).__init__()
        self.recv_queue = recv_queue
        self.send_queue = send_queue

    def run(self):
        while True:
            msg = self.recv_queue.get()
            if msg is not None:
                msg.direction = msg.direction[1:]
                # here also can put msg to a worker thread
                self.send_queue.put(msg)
            time.sleep(1)
