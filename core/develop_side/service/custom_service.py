# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 tianyou pan <sherry0429 at SOAPython>
this class make a example, when we need define service's build method (don't use base build)

the base build doing:
1.make working path
2.copy exe scripts from egg_template
3.get input file in param template
4.reload handler and set it to service template
5.prepare input file,
that means if input file param is dir,
if it's will copy, if it's ftp, it's will download,
also, you can redefine it by rewrite method 'prepare_input_file'

and for example:

build()
    f_ = open(path)
    f_.write()

and read f_ in your callback:

file_change_callback()
    f_ = open(path)
    stream = f_.read()
"""
from template import ServiceProgramTemplate
from data_transfor import DataTransfor


class CustomService(ServiceProgramTemplate):

    def __init__(self):
        super(CustomService, self).__init__()

    def build(self):
        # call this first, make sure all bases operation done there
        super(CustomService, self).build()
        pass

    def prepare_input_file(self):
        DataTransfor.get_file(self.param_template.g_input_file)
