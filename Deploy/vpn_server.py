#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import os
import platform
import shutil
from vpn_conf import VpnConf
from vpn_logger import VpnLog

class VpnServer(object):
    """
    Manage VPN tenant server
    """
    
    __sys = platform.system()
    
    __SH_VPN = "openvpn"
    __SH_SOURCE = "source"
    __SH_VARS = "vars"
    __SH_CLEAN = "clean-all"
    __SH_CA = "build-ca"
    __SH_DH = "build-dh"
    __SH_SERVER = "build-key-server"
    __SH_CLIENT = "build-key"
    __OP_BATCH = "--batch"
    __OP_SECRET = "--secret"
    __OP_GENKEY = "--genkey"

    def __init__(self, name, path, log):
        self.__name = name
        self.__dir_path = path
        self.__config_dir = self.__dir_path + "/config/"
        self.__key_dir = self.__dir_path + "/key/"
        self.__log_dir = self.__dir_path + "/log/"
        self.__conf_list = []
        self.__vpn_log = VpnLog(log)

    def __create_dir(self, rsa):
        if self.__sys == "Windows":
            os.makedirs(self.__dir_path)
            cp_cmd = r"xcopy /S " + rsa + r"\*" + self.__dir_path
            os.system(cp_cmd)
            os.makedirs(self.__config_dir)
            os.makedirs(self.__log_dir)
        else:
            os.makedirs(self.__dir_path, 0o755)
            cp_cmd = "cp " + rsa + "/* " + self.__dir_path
            os.system(cp_cmd)
            os.makedirs(self.__config_dir, 0o755)
            os.makedirs(self.__log_dir, 0o755)

    def __sh_build_ca(self, op = __OP_BATCH, param = self.__name):
        """
        build-ca
        """

        cmd = "./" + self.__SH_CA + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_dh(self, op = "", param = ""):
        """
        build-dh
        """

        cmd = "./" + self.__SH_DH + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_server(self, op = self.__OP_BATCH, param = self.__name):
        """
        build-key-server
        """

        cmd = "./" + self.__SH_SERVER + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_client(self, op = self.__OP_BATCH, param = ""):
        """
        build-key
        """

        cmd = "./" + self.__SH_CLIENT + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_clean(self, op = "", param = ""):
        """
        build-key
        """

        cmd = "./" + self.__SH_CLEAN + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __vpn_shell(self, sh, param):
        """
        Execute vpn shell 
        @sh: command name
        @param: dic [op:param]
        """

        cmd = sh + " "

        for key in param:
            cmd += key + " " + param[key] + " "

        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __create_keys(self):
        os.chdir(self.__dir_path)
        __vpn_shell(self.__SH_SOURCE, {"":"./" + self.__SH_VARS})
        __vpn_shell("chmod", {"-R 755":"./keys"})
        __sh_clean()
        __sh_build_ca()
        __sh_build_server()
        __sh_build_dh()
        __vpn_shell(self.__SH_VPN, 
                    {self.__OP_GENKEY:"", self.__OP_SECRET:"./keys/ta.key"})
        __vpn_shell("chmod", {"644":"./keys/ta.key"})

    def __copy_keys(self):
        shutil.copy(self.__key_dir + "/ca.crt", \
                    self.__config_dir)
        shutil.copy(self.__key_dir + "/ca.key", \
                    self.__config_dir)
        shutil.copy(self.__key_dir + "/ta.key", \
                    self.__config_dir)
        if os.path.isfile(self.__key_dir + "/dh1024.pem"):
            shutil.copy(self.__key_dir + "/dh1024.pem", \
                        self.__config_dir)
        else:
            shutil.copy(self.__key_dir + "/dh2048.pem", \
                        self.__config_dir)
        shutil.copy(self.__key_dir + self.__name + ".crt", \
                    self.__config_dir)
        shutil.copy(self.__key_dir + self.__name + ".key", \
                    self.__config_dir)

    def _set_conf_attr(self, vpn_cf, key, attr):
          
        if key == VpnConf.TAG_PORT:
            vpn_cf.set_port_var(attr)
        elif key == VpnConf.TAG_PROTO:
            vpn_cf.set_proto_var(attr)
        elif key == VpnConf.TAG_DEV:
            vpn_cf.set_dev_var(attr)
        elif key == VpnConf.TAG_CA:
            vpn_cf.set_ca_var(attr)
        elif key == VpnConf.TAG_CERT:
            vpn_cf.set_cert_var(attr)
        elif key == VpnConf.TAG_KEY:
            vpn_cf.set_key_var(attr)
        elif key == VpnConf.TAG_dh:
            vpn_cf.set_dh_var(attr)
        elif key == VpnConf.TAG_SERVER:
            vpn_cf.set_server_var(attr)
        elif key == VpnConf.TAG_IPPOOL:
            vpn_cf.set_ippool_var(attr)
        elif key == VpnConf.TAG_C2C:
            vpn_cf.set_c2c_var(attr)
        elif key == VpnConf.TAG_KALIVE:
            vpn_cf.set_kalive_var(attr)
        elif key == VpnConf.TAG_TLS:
            vpn_cf.set_tls_var(attr)
        elif key == VpnConf.TAG_MAXC:
            vpn_cf.set_maxc_var(attr)
        elif key == VpnConf.TAG_STATUS:
            vpn_cf.set_status_var(attr)
        elif key == VpnConf.TAG_LOG:
            vpn_cf.set_log_var(attr)
    
    def vpn_create(self, rsa):
        """
        Create a directory by self
        @xml: xml file path
        @rsa: easy-rsa shell path
        """
        if os.path.exists(self.__dir_path):
            log_str = "The '" + self.__name + "' directory is existed."
            self.__vpn_log.write_ex(log_str)
            return False

        __create_dir(rsa)
        log_str = "Create '" + self.__name + "' directory successfully."
        self.__vpn_log.write_ex(log_str)

        __create_keys()
        __copy_keys()
        log_str = "Create '" + self._name + "' keys successfully."

        return True

    def vpn_add_server_ex(self, vpn_conf):
        """
        Add a new server with 'VpnConf'
        @vpn_conf: 'VpnConf' object
        """
        self.__conf_list.append(vpn_conf)

    def vpn_add_server(self, template, name, conf_dic):
        """
        Build a new server with 'conf_dic' config
        @template: server config template path
        @name: server config file name
        @conf_dic: server config options dictionary
        """
        shutil.copy(template, self.__config_dir + name)

        vpn_cf = VpnConf(self.__config_dir + name)

        for key in conf_dic:
            if not conf_dic[key]:
                self._set_conf_attr(vpn_cf, key, conf_dic[key])
        vpn_cf.conf_flush()

        self.__conf_list.append(vpn_cf)

    def get_config_list(self):
        """
        Get the object list of the config
        """
        return self.__conf_list

if __name__ == "__main__":
    print "test"
    pass