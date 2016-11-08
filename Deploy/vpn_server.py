#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import os
import platform
from vpn_conf import VpnConf
from vpn_logger import VpnLog

class VpnServer(object):
    """
    Manage VPN tenant server
    """
    
    __sys = platform.system()

    def __init__(self, name, path, xml, log):
        self.__name = name
        self.__dir_path = path
        self.__xml_path = xml
        self.__conf_list = []
        self.__vpn_log = VpnLog(log)

    def get_config_obj(self):
        """
        Get the object of the config
        """
        pass
    
    def __xml_add_tenant(self, name, path):

        pass

    def vpn_create(self, xml, rsa):
        """
        Create a directory by self
        """
        if os.path.exists(self.__dir_path):
            log_str = "The '" + self.__name + "' directory is existed."
            self.__vpn_log.write_info(log_str)
            return False

        if self.__sys == "Windows":
            os.makedirs(self.__dir_path)
            cp_cmd = r"xcopy /S " + rsa + r"\*" + self.__dir_path
            os.system(cp_cmd)
            os.makedirs(self.__dir_path + "/config")
            os.makedirs(self.__dir_path + "/log")

        else:
            os.makedirs(self.__dir_path, 0o755)
            cp_cmd = "cp " + rsa + "/* " + self.__dir_path
            os.system(cp_cmd)
            os.makedirs(self.__dir_path + "/config", 0o755)
            os.makedirs(self.__dir_path + "/log", 0o755)



        log_str = "Create '" + self.__name + "' directory successfully."
        self.__vpn_log.write_info(log_str)



        return True

if __name__ == "__main__":
    print "test"
    pass