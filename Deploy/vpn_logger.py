#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import logging
import logging.config

class VpnLog:

    #self.__path: the path of the log file
    LOG_D = 'D'
    LOG_I = 'I'
    LOG_E = 'E'
    LOG_W = 'W'
    LOG_C = 'C'

    def __init__(self, conf, name = "root"):
        self.__path = conf
        logging.config.fileConfig(conf)
        self.logger = logging.getLogger(name)

    def write_debug(self, info):
        self.logger.debug(info)

    def write_info(self, info):
        self.logger.info(info)

    def write_warn(self, info):
        self.logger.warning(info)

    def write_error(self, info):
        self.logger.error(info)

    def write_critical(self, info):
        self.logger.critical(info)

    def write_ex(self, info, ex = "=====", flag = 'I'):
        lg = ex + info + ex

        if flag == self.LOG_D:
            self.write_debug(lg)

        if flag == self.LOG_I:
            self.write_info(lg)
        
        if flag == self.LOG_W:
            self.write_warn(lg)
        
        if flag == self.LOG_E:
            self.write_error(lg)
        
        if flag == self.LOG_C:
            self.write_critical(lg)