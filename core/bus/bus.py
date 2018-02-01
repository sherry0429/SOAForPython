# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from threading import Thread
import time
from common import PickleUtil
from common import RedisUtil
from message import BaseMessage


class MsgBus(object):

    access_modules = set()

    def __init__(self, conf):
        self.redis = RedisUtil(conf['redis']['ip'],
                               conf['redis']['port'],
                               conf['redis']['db'])

    def start(self):
        m_th = MsgReceiver(self.redis, self.access_modules)
        m_th.start()


class MsgReceiver(Thread):

    def __init__(self, redis, access_modules):
        super(MsgReceiver, self).__init__()
        self.redis = redis
        self.access_modules = access_modules

    def run(self):
        while True:
            msg = self.redis.rpop('bus')
            if msg is not None:
                # use Controller, to judge every msg
                content = PickleUtil().p_decode(msg)
                if isinstance(content, BaseMessage):
                    if content.before is not None:
                        self.access_modules.add(content.before)
                    if len(content.direction) != 0:
                        direction = content.direction[0]
                        self.redis.lpush('bus-%s' % direction.lower(), msg)
            time.sleep(1)


if __name__ == '__main__':
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    try:
        print "Msg Bus Start ..."
        engine = MsgBus(conf_dict)
        engine.start()
    except Exception, error_msg:
        print error_msg
        print "Msg Bus Start Failed"
