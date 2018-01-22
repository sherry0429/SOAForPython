# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from param import ServiceParamTemplate
from service import ServiceProgramTemplate
import redis
import pickle



if __name__ == '__main__':
    service_A = ServiceProgramTemplate()
    service_A.set_param_template(ServiceParamTemplate())
    redis = redis.StrictRedis('localhost', '6379', 0)
    redis.lpush('service-pipe', pickle.dumps(service_A))