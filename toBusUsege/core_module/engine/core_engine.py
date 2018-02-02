# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import time
from threading import Thread
from toBus import ModuleBase


class CoreEngineModule(ModuleBase):

    def __init__(self, redis_ip, redis_port, redis_db, module_name):
        super(CoreEngineModule, self).__init__(redis_ip, redis_port, redis_db, module_name)

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
