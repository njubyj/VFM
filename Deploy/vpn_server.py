#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import os,sys
import platform
import shutil
from vpn_conf import VpnConf
from vpn_logger import VpnLog
from vpn_base import VpnBase

class VpnServer(VpnBase):
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
        self.__vpn = "openvpn"
        self.__name = name
        self.__dir_path = path
        self.__config_dir = self.__dir_path + "/config/"
        self.__key_dir = self.__dir_path + "/keys/"
        self.__log_dir = self.__dir_path + "/log/"
        self.__conf_list = []
        self.__vpn_log = VpnLog(log)

        if self.__sys == "Windows":
            self.__dir_path = self.__dir_path.replace('/', '\\\\')
            self.__config_dir = self.__config_dir.replace('/', '\\\\')
            self.__key_dir = self.__key_dir.replace('/', '\\\\')
            self.__log_dir = self.__log_dir.replace('/', '\\\\')

    def __create_dir(self, rsa):
        if self.__sys == "Windows":
            os.makedirs(self.__dir_path)
            cp_cmd = 'xcopy /S "' + rsa + r'*" "' + self.__dir_path + '"'
            os.system(cp_cmd)
            os.makedirs(self.__config_dir)
            os.makedirs(self.__log_dir)
        else:
            os.makedirs(self.__dir_path, 0o755)
            cp_cmd = "cp " + rsa + "/* " + self.__dir_path
            os.system(cp_cmd)
            os.makedirs(self.__config_dir, 0o755)
            os.makedirs(self.__log_dir, 0o755)

    def __sh_vars(self):
        """
        source ./vars | vars
        """
        cmd = ""
        if self.__sys == "Windows":
            cmd += self.__SH_VARS
        else:
            cmd += self.__SH_SOURCE + " ./" + self.__SH_VARS

        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_ca(self, op, param):
        """
        build-ca
        """
        cmd = ""
        if not self.__sys == "Windows":
            cmd += "./"
        else:
            cmd += "vars && "

        cmd += self.__SH_CA + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_dh(self, op = "", param = ""):
        """
        build-dh
        """
        cmd = ""
        if not self.__sys == "Windows":
            cmd += "./"
        else:
            cmd += "vars && "

        cmd += self.__SH_DH + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_server(self, op, param):
        """
        build-key-server
        """
        cmd = ""
        if not self.__sys == "Windows":
            cmd += "./"
        else:
            cmd += "vars && "

        cmd += self.__SH_SERVER + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_build_client(self, op, param):
        """
        build-key
        """
        cmd = ""
        if not self.__sys == "Windows":
            cmd += "./"
        else:
            cmd += "vars && "

        cmd += self.__SH_CLIENT + " " + op + " " + param
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __sh_clean(self, op = "", param = ""):
        """
        clean-all
        """
        cmd = ""
        if not self.__sys == "Windows":
            cmd += "./"
        else:
            cmd += "vars && "

        cmd += self.__SH_CLEAN + " " + op + " " + param 
        
        res = os.system(cmd)

        if res != 0:
            return False

        return True

    def __create_keys(self):
        os.chdir(self.__dir_path)
        self.__sh_vars()
        self.__sh_clean()
        if not self.__sys == "Windows":
            self.vpn_shell("chmod", {"-R 755":"./keys"})
        if self.__sys == "Windows":
            self.__sh_build_ca("", self.__name)
            self.__sh_build_server("", self.__name)
        else:
            self.__sh_build_ca(self.__OP_BATCH, self.__name)
            self.__sh_build_server(self.__OP_BATCH, self.__name)
        self.__sh_build_dh()
        self.vpn_shell(self.__SH_VPN, \
            {self.__OP_GENKEY:"", self.__OP_SECRET:self.__key_dir + "ta.key"})
        if not self.__sys == "Windows":
            self.vpn_shell("chmod", {"644":"./keys/ta.key"})

    def __copy_keys(self):
        shutil.copy(self.__key_dir + "ca.crt", \
                    self.__config_dir)
        shutil.copy(self.__key_dir + "ca.key", \
                    self.__config_dir)
        shutil.copy(self.__key_dir + "ta.key", \
                    self.__config_dir)
        if os.path.isfile(self.__key_dir + "dh1024.pem"):
            shutil.copy(self.__key_dir + "dh1024.pem", \
                        self.__config_dir)
        else:
            shutil.copy(self.__key_dir + "dh2048.pem", \
                        self.__config_dir)
        shutil.copy(self.__key_dir + self.__name + ".crt", \
                    self.__config_dir)
        shutil.copy(self.__key_dir + self.__name + ".key", \
                    self.__config_dir)

    def __set_conf_attr(self, vpn_cf, key, attr):
          
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
        elif key == VpnConf.TAG_DH:
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

    def set_vpn(self, vpn):
        """
        Set VPN excute path
        @vpn: vpn path
        """
        self.__vpn = vpn

    def get_vpn(self):
        """
        Get VPN excute path
        """
        return self.__vpn
    
    def vpn_create(self, rsa):
        """
        Create a directory by self
        @rsa: easy-rsa shell path
        """
        if os.path.exists(self.__dir_path):
            log_str = "The '" + self.__name + "' directory is existed."
            self.__vpn_log.write_ex(log_str)
            return False

        self.__create_dir(rsa)
        log_str = "Create '" + self.__name + "' directory successfully."
        self.__vpn_log.write_ex(log_str)

        self.__create_keys()
        self.__copy_keys()
        log_str = "Create '" + self._name + "' keys successfully."

        return True

    def vpn_add_server(self, template, name, conf_dic):
        """
        Build a new server with 'conf_dic' config
        @template: server config template path
        @name: server config file name
        @conf_dic: server config options dictionary
        """
        if self.__sys == "Windows":
            shutil.copy(template, self.__config_dir + name + ".ovpn")
            vpn_cf = VpnConf(self.__config_dir + name + ".ovpn")
        else:
            shutil.copy(template, self.__config_dir + name + ".conf")
            vpn_cf = VpnConf(self.__config_dir + name + ".conf")


        for key in conf_dic:
            if conf_dic[key]:
                self.__set_conf_attr(vpn_cf, key, conf_dic[key])
        vpn_cf.conf_flush()

        self.__conf_list.append(vpn_cf)

    def get_config_list(self):
        """
        Get the object list of the config
        """
        return self.__conf_list

    def vpn_start(self):
        """
        Start server list
        """
        for conf in self.__conf_list:
            if not self.__sys == "Windows":
                param_dic = {"--daemon --writepid":'"' + self.__log_dir + self.__name + ".pid\"", \
                    "--config":'"' + conf.get_path() + '"'}
            else:
                param_dic = {"--writepid":'"' + self.__log_dir + self.__name + ".pid\"", \
                    "--config":'"' + conf.get_path() + '"'}

        try:
            pid = os.fork()

            if 0 == pid:
                self.vpn_shell(self.__vpn, param_dic)

            else:
                pass

    def vpn_add_client(self, param = "--batch", name = "client"):
        """
        Build a client certification
        @param: parameters for 'build-key'
        @name: client name
        """
        os.chdir(self.__dir_path)

        cmd = ""
        if self.__sys != "Windows":
            cmd += "./"
        
        cmd += self.__SH_CLIENT + " " + param + " " + name

        res = os.system(cmd)

        if res != 0:
            return False

        return True


if __name__ == "__main__":

    #shutil.rmtree(r"E:\vpn", ignore_errors = True)
    vus = VpnServer("test", "E:\\\\vpn", r".\Resource\vpn_logging.conf")
    vus.vpn_create("D:\\Program Files\\OpenVPN\\easy-rsa\\")

    conf_dic = {\
        VpnConf.TAG_PORT:"port 1194", \
        VpnConf.TAG_PROTO:"proto udp", \
        VpnConf.TAG_DEV:"dev tap", \
        VpnConf.TAG_CA:r'ca "E:\\\\vpn\\\\config\\\\ca.crt"', \
        VpnConf.TAG_CERT:r'cert "E:\\\\vpn\\\\config\\\\test.crt"', \
        VpnConf.TAG_KEY:r'key "E:\\\\vpn\\\\config\\\\test.key"', \
        VpnConf.TAG_DH:r'dh "E:\\\\vpn\\\\config\\\\dh1024.pem"', \
        VpnConf.TAG_SERVER:"server 10.8.8.0 255.255.255.0", \
        VpnConf.TAG_IPPOOL:r'ifconfig-pool-persist "E:\\\\vpn\\\\log\\\\ipp.txt"', \
        VpnConf.TAG_C2C:"client-to-client", \
        VpnConf.TAG_KALIVE:"keepalive 10 120", \
        VpnConf.TAG_TLS:r'tls-auth "E:\\\\vpn\\\\config\\\\ta.key"', \
        VpnConf.TAG_MAXC:";max-clients 100", \
        VpnConf.TAG_STATUS:r'status "E:\\\\vpn\\\\log\\\\openvpn-status.log"', \
        VpnConf.TAG_LOG:r'log "E:\\\\vpn\\\\log\\\\openvpn.log"'\
    }

    vus.vpn_add_server(".\\Resource\\server.conf", "server", conf_dic)
    vus.vpn_start()

    print str