# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""
from common import WatcherHandler


class SERVICETESTHandler(WatcherHandler):

    def __init__(self):
        super(SERVICETESTHandler, self).__init__()

    def file_change_callback(self, file_list, service_instance):
        print file_list
        return

    def after_watch_callback(self, file_list, service_instance):
        print file_list
        return

    def before_watch_callback(self, service_instance):
        pass

