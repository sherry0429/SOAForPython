# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from threading import Thread
import time
import pickle
import redis
from base_msg import BaseMessage


class MsgBus(object):

    access_modules = set()

    def __init__(self, redis_ip,  redis_port, redis_db):
        self.redis_ip = redis_ip
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis = redis.StrictRedis(redis_ip,
                                       redis_port,
                                       redis_db)

    def start(self):
        m_th = MsgReceiver(self.redis, self.access_modules, self.msg_recv_callback, self.msg_send_callback)
        m_th.start()
        print "bus with redis %s:%s:%s start" % (self.redis_ip, str(self.redis_port), str(self.redis_db))

    def msg_recv_callback(self, msg):
        pass

    def msg_send_callback(self, msg):
        pass


class MsgReceiver(Thread):

    def __init__(self, redis, access_modules, msg_recv_callback, msg_send_callback):
        super(MsgReceiver, self).__init__()
        self.redis = redis
        self.access_modules = access_modules
        self.msg_recv_callback = msg_recv_callback
        self.msg_send_callback = msg_send_callback

    def run(self):
        while True:
            msg = self.redis.rpop('bus')
            if msg is not None:
                # use Controller, to judge every msg
                content = pickle.loads(msg)
                self.msg_recv_callback(content)
                if isinstance(content.__class__.__bases__[0], BaseMessage):
                    if content.before is not None:
                        self.access_modules.add(content.before)
                    if len(content.direction) != 0:
                        if content.publish_module_type is not None:
                            content.direction = list()
                            self.redis.publish('%s' % content.publish_module_type)
                        else:
                            direction = content.direction[0]
                            self.redis.lpush('bus-%s' % direction.lower(), msg)
                        self.msg_send_callback(content)
            time.sleep(1)

