# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this example for call multi services and each of them delay other
"""
from src import ServiceParamTemplate
import redis
from scheduler import ParamScheduler


if __name__ == '__main__':
    """
    how client know services's path ? it's not a big problem,
    just record all services name in redis / database, client get it, and use relative path access them.
    """
    # monitor conf
    conf_dict = dict()
    conf_dict['redis'] = dict()
    conf_dict['redis']['ip'] = 'localhost'
    conf_dict['redis']['port'] = 6379
    conf_dict['redis']['db'] = 0
    redis = redis.StrictRedis('localhost', '6379', 0)
    services = {
        'servicepool/servicetest.py': 'servicetest.py',
        'servicepool/servicetesttwo.py': 'servicetesttwo.py'
    }
    for (k, v) in services.items():
        """
        if work_path is same, all services will be copy to same directory
        in this case, we copy two services in save work path and start them. if first failed, we stop second.
        """
        param_template = ServiceParamTemplate(work_path='work',
                                              service_path=k,
                                              input_file='a',
                                              output_file='b',
                                              s_service_name=v)
        schduler = ParamScheduler(conf_dict)
        service_id = param_template.g_service_id
        redis.lpush('service-pipe', schduler.encode_param(param_template))
        code = None
        while True:
            code = redis.hget('services', service_id)
            if code is not None:
                break
        if code != 0:
            print "service %s failed" % service_id
            break
    print "all services done here"
