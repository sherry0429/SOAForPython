# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
"""


class WatcherHandler(object):

    def __init__(self):
        pass

    def before_watch_callback(self, service_instance):
        """
        here define some operation before watcher start
        :return:
        """
        pass

    def file_change_callback(self, file_list, service_instance):
        """
        this callback will return file_list in work_dir every sec
        use this callback to make sure serivce's progress
        :return:
        """
        pass

    def after_watch_callback(self, file_list, service_instance):
        """
        this callback be called before watcher thread stop.
        it's will return all file_list this thread spawn.
        use this callback can make data recycle logical
        :return:
        """
        pass