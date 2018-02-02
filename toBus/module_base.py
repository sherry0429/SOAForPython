# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
import redis
from Queue import Queue
from transport_util import MsgSenderToBus, MsgReceiverFromBus, PublishMsgReceiverFromBus


class ModuleBase(object):

    def __init__(self, redis_ip, redis_port, redis_db, module_name, module_type=None):
        self.redis = redis.StrictRedis(redis_ip, redis_port, redis_db)
        self.module_name = module_name
        self.module_type = module_type
        self.send_queue = Queue()
        self.recv_queue = Queue()
        self.sender_th = MsgSenderToBus(self.redis, self.module_name, self.module_type, self.send_queue)
        self.receiver_th = MsgReceiverFromBus(self.redis, self.module_name, self.module_type, self.recv_queue)
        self.sender_th.start()
        print "module %s sender thread start" % module_name
        self.receiver_th.start()
        print "module %s receiver thread start" % module_name
        if self.module_type is not None:
            self.pubsub = self.redis.pubsub()
            self.pubsub.subscribe(self.module_type)
            self.publish_receiver_th = PublishMsgReceiverFromBus(self.pubsub, self.module_name, self.module_type, self.recv_queue)
            self.publish_receiver_th.start()
            print "module %s publish receiver thread start" % module_name