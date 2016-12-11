#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import os
import sys
import shutil
import getopt
import xml.etree.ElementTree as ET
import vpn_global_var as G
from vpn_xml import VpnXml as VXML
from vpn_guide import VpnGuideParser as VGP
from vpn_tag import VpnTag as VTAG
from vpn_logger import VpnLog as VLOG
from vpn_server import VpnServer as VSEV

class VpnDeploy(object):
    """
    Vpn depoy 
    """

    # self.__args: arguments dictionary
    # self.__conf: guide config path
    # self.__log: log
    # self.__xml: xml
    # self.__guide: guide

    def __init__(self, argv):
        self.__argv = argv 
        self.__args = {}
        self.__xml_path = G.vpn_xml_path
        self.__log = self.__guide = None
        self.__confxml = self.__dataxml = None
        self.__cloud = ""
        self.__vpn_dir = ""
        self.__rsa = ""
        self.__guide_path = ""
        self.__log_conf = ""
        self.__template = ""
        self.__dxml_path = ""
        self.__usr_dic = {}
        self.__CONF_SUF = VTAG.VPN_CONF
        self.init()

    def show_usage(self):
        """
        Show usage
        """
        
        print "None"
        
    def parse_argv(self):
        """
        Parse arguments
        """
        args_str = "h"
        args_list = ["help", "conf="]
        opt, args = getopt.getopt(self.__argv[1:], args_str, args_list)

        for op, arg in opt:
            if op == "-h" or op == "--help":
                self.show_usage()
            if op == "--conf":
                self.__args[op] = arg

    #def get_args(self):
    #    """
    #    Get arguments dictionary
    #    """
    #    return self.__args

    def __verify_usr_dir(self, usr_dir):
        config_dir = usr_dir + '/' + VTAG.DIR_CONFIG
        for file in os.listdir(config_dir):
            if self.__CONF_SUF in file:
                return True
        return False

    def __add_usr(self, usr):
        usr_obj = self.__usr_dic[usr]
        usr_dir = usr_obj.get_usr_dir()
        if not os.path.exists(usr_dir):
            if self.__dataxml.is_usr_exist(usr):
                # delete a usr element in the xml file
                self.__dataxml.xml_del_usr(usr)

            flag = raw_input("There is no directory of '" + usr + "'. " + \
                "Do you want to create a new one?[y/n]:")
            if flag == 'y':
                # add a usr element in the xml file
                idx = self.__confxml.find(VTAG.XML_TAG_USRIDX)
                usr_obj.vpn_create(self.__rsa)
                self.__dataxml.xml_add_usr(usr, idx.text, usr_dir)
                idx.text = str(int(idx.text) + 1)
                self.__confxml.write(self.__xml_path, encoding = "utf-8")
            else:
                self.__log.write_error("The '" + usr + "' is lack of directory.")
                return False
        else:
            # check xml file record
            ## not: check directory correctness
            ### no: delete + create 
            ### yes： completation 
            if not self.__dataxml.is_usr_exist(usr):
                if not self.__verify_usr_dir(usr_dir):
                    shutil.rmtree(usr_dir)
                    idx = self.__confxml.find(VTAG.XML_TAG_USRIDX)
                    usr_obj.vpn_create(self.__rsa)
                    self.__dataxml.xml_add_usr(usr, idx.text, usr_dir)
                    idx.text = str(int(idx.text) + 1)
                    self.__confxml.write(self.__xml_path, encoding = "utf-8")
                else:
                    ## ...
                    pass

        return True

    def __add_server_default(self, usr):
        self.__add_usr(usr)
        usr_obj = self.__usr_dic[usr]
        usr_dir = usr_obj.get_usr_dir()
        conf_dir = usr_dir + '/' + VTAG.DIR_CONFIG + '/'
        log_dir = usr_dir + '/' + VTAG.DIR_LOG + '/'
        ca_crt = conf_dir + VTAG.CA_CRT
        ca_key = conf_dir + VTAG.CA_KEY
        sev_crt = conf_dir + usr + VTAG.SUF_CRT
        sev_key = conf_dir + usr + VTAG.SUF_KEY
        dh_pem = conf_dir + VTAG.DH_PEM1
        ta_key = conf_dir + VTAG.TA_KEY
        tap_idx = self.__confxml.findtext(VTAG.XML_TAG_TAPIDX)
        addr_idx = self.__confxml.findtext(VTAG.XML_TAG_ADDRIDX)
        port_idx = self.__confxml.findtext(VTAG.XML_TAG_PORTIDX)
        sev_idx = self.__dataxml.get_usr_sevidx(usr)
        sev_ips = addr_idx + ' ' + VTAG.IP_MASK8
        ser_name = VTAG.SEV_NAME + str(sev_idx) 
        log_pre = log_dir + ser_name + '_'
        ip_pool = log_pre + VTAG.SIGN_IPP + VTAG.SUF_TXT
        log_status = log_pre + VTAG.SIGN_STATUS + VTAG.SUF_LOG
        log_log = log_pre + VTAG.SIGN_LOG + VTAG.SUF_LOG
        conf_dic[VTAG.TAG_PORT] = VTAG.TAG_PORT + ' ' + port_idx
        conf_dic[VTAG.TAG_DEV] = VTAG.TAG_DEV + ' ' + VTAG.DEV_TAP + tap_idx
        conf_dic[VTAG.TAG_SERVER] = VTAG.TAG_SERVER + ' ' + sev_ips
        conf_dic[VTAG.TAG_CA] = VTAG.TAG_CA + ' ' + ca_crt
        conf_dic[VTAG.TAG_CERT] = VTAG.TAG_CERT + ' ' + sev_crt
        conf_dic[VTAG.TAG_KEY] = VTAG.TAG_KEY + ' ' + sev_key
        conf_dic[VTAG.TAG_DH] = VTAG.TAG_DH + ' ' + dh_pem
        conf_dic[VTAG.TAG_TLS] = VTAG.TAG_TLS + ' ' + ta_key
        conf_dic[VTAG.TAG_IPPOOL] = VTAG.TAG_IPPOOL + ' ' + ip_pool
        conf_dic[VTAG.TAG_STAUS] = VTAG.TAG_STAUS + ' ' + log_status
        conf_dic[VTAG.TAG_LOG] = VTAG.TAG_LOG + ' ' + log_log
        usr_obj.vpn_add_server(self.__template, ser_name, conf_dic)

        # add a server for the user in the xml file


    def __args_default(self):
        self.__dxml_path = self.__confxml.findtext(VTAG.XML_TAG_DATAXML)
        self.__dataxml = VXML(self.__dxml_path)
        if not os.path.isfile(self.__dxml_path):
            self.__dataxml.xml_create() 
        self.__guide_path = self.__confxml.findtext(VTAG.XML_TAG_GUIDE)
        if not os.path.isfile(self.__guide_path):
            self.__log.write_error("Lack of guide config file.")
            return False
        self.__guide = VGP(self.__guide_path)
        sev_list = self.__guide.get_servers()
        clt_list = self.__guide.get_clients()

        for sev in sev_list:
            usr_n = sev[0]
            op_dic = sev[1]
            task = op_dic[VTAG.OPT_TASK]
            
            usr_obj = VSEV(usr_n, self.__vpn_dir + "/z_" + usr_n, self.__log_conf)
            self.__usr_dic[usr_n] = usr_obj
                          
            if task == VTAG.TASK_ADD:
                # add server default
                pass

    def init(self):
        """
        Init deploy environment
        """
        if not os.path.isfile(self.__xml_path):
            print "[ERROR]: Lack of config.xml."
            return False

        self.__confxml = ET.parse(self.__xml_path)
        self.__cloud = self.__confxml.findtext(VTAG.XML_TAG_CLOUD)
        self.__vpn_dir = self.__confxml.findtext(VTAG.XML_TAG_VPNDIR)
        self.__rsa = self.__confxml.findtext(VTAG.XML_TAG_RSA)
        if not os.path.exists(self.__rsa):
            print "[ERROR]: Lack of easy-rsa scripts."
            return False
        self.__log_conf = self.__confxml.findtext(VTAG.XML_TAG_LOGGER)
        if not os.path.isfile(self.__log_conf):
            print "[ERROR]: Lack of log config file."
            return False
        self.__log = VLOG(self.__log_conf, "deploy")
        self.__template = self.__confxml.findtext(VTAG.XML_TAG_TEMPLATE)
        if not os.path.isfile(self.__template):
            print "[ERROR]: Lack of log template file."
            return False


    def excute(self):
        """
        Excute operations 
        """
        self.init()
        self.parse_argv()

        if not self.__args:
            
            # args default
            pass
            



if __name__ == "__main__":

    
    pass