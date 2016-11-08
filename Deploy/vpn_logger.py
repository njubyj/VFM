#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import logging
import logging.config

class VpnLog:
    def __init__(self, conf, name = "root"):
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