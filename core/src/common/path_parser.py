# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""


class PathParser(object):

    SYSTEM = 1
    FTP = 2
    MYSQL = 3
    REDIS = 4

    def __init__(self):
        pass

    @classmethod
    def parse_path(cls, path):
        if "ftp://" in path:
            return cls.FTP
        elif "mysql://" in path:
            return cls.MYSQL
        elif "redis://" in path:
            return cls.REDIS
        else:
            return cls.SYSTEM
