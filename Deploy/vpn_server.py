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
    
    __SH_CA = "build-ca"
    __SH_DH = "build-dh"
    __SH_SERVER = "build-key-server"
    __SH_CLIETN = "build-key"
    __OP_BATCH = "--batch"
    __OP_SECRET = "--secret"
    __OP_GENKEY = "--genkey"

    def __init__(self, name, path, log):
        self.__name = name
        self.__dir_path = path
        self.__conf_list = []
        self.__vpn_log = VpnLog(log)

    def get_config_obj(self):
        """
        Get the object of the config
        """
        pass

    def __create_dir(self, rsa):
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

    def __vpn_shell(self, sh, param):
        """
        Execute vpn shell 
        @sh: command name
        @param: dic [op:param]
        """

        cmd = sh + ' '

        for key in param:
            cmd += key + ' ' + param[key] + ' ' 

        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __create_keys(self):
        pass
    
    def vpn_create(self, rsa):
        """
        Create a directory by self
        @xml: xml file path
        @rsa: easy-rsa shell path
        """
        if os.path.exists(self.__dir_path):
            log_str = "The '" + self.__name + "' directory is existed."
            self.__vpn_log.write_info(log_str)
            return False

        __create_dir(rsa)
        log_str = "Create '" + self.__name + "' directory successfully."
        self.__vpn_log.write_info(log_str)



        return True



    def vpn_add_server(self):
        pass

if __name__ == "__main__":
    print "test"
    pass