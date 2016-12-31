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
    # self.__xml_path: config xml file path
    # self.__log: log handle
    # self.__guide: guild config handle
    # self.__confxml: config xml handle
    # self.__dataxml: data xml handle
    # self.__cloud: cloud server address
    # self.__vpn_dir: vpn deploy root directory
    # self.__rsa: vpn build scripts directory
    # self.__guide_path: guide config file path
    # self.__log_conf: log config file path
    # self.__template: server config file path
    # self.__dxml_path: data xml file path
    # self.__usr_dic: user objects' handles dictionary
    # self.__guide_path: guide config path

    __ARG_CONF = "--conf"

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

    def __check_usr(self, usr):
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
                usr_idx = idx.text
                idx.text = str(int(idx.text) + 1)
                self.__confxml.write(self.__xml_path, encoding = "utf-8")
                usr_obj.vpn_create(self.__rsa)
                self.__dataxml.xml_add_usr(usr, usr_idx, usr_dir)
                
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
                    pass

        return True

    def __confirm_sev_name(self, usr, conf):
        name = ""
        if not conf.has_key(VTAG.OPT_NAME):
            sev_idx = self.__dataxml.get_usr_sevidx(usr)
            if sev_idx is None:
                self.__log.write_error("The user '%s' is none." % usr)
                return name
            name = VTAG.SEV_NAME + str(sev_idx) 
        else:
            name = conf[VTAG.OPT_NAME]

        return name

    def __detect_tap(self, tap):
        if tap in self.__dataxml.get_devs():
            return True
        else:
            return False

    def __detect_port(self, port):
        if port in self.__dataxml.get_ports():
            return True
        else:
            return False

    def __format_ip(self, ip, mask):
        ips = ip.split('.', 3)
        masks = mask.split('.', 3)

        ips[0] = str(int(ips[0]) & int(masks[0]))
        ips[1] = str(int(ips[1]) & int(masks[1]))
        ips[2] = str(int(ips[2]) & int(masks[2]))
        ips[3] = str(int(ips[3]) & int(masks[3]))

        return ".".join(ips)

    def __detect_ip(self, ip, mask):
        ip = self.__format_ip(ip, mask)
        for (ipt, maskt) in self.__dataxml.get_ips():
            if ipt == ip:
                return True

        return False

    def __get_tapidx(self):
        idx = self.__confxml.findtext(VTAG.XML_TAG_TAPIDX)
        taps = self.__dataxml.get_devs()
        tap = VTAG.DEV_TAP + idx
        while tap in taps:
            idx = str(int(idx) + 1)
            tap = VTAG.DEV_TAP + idx 
        self.__confxml.find(VTAG.XML_TAG_TAPIDX).text = str(int(idx) + 1)
        self.__confxml.write(self.__xml_path, encoding = "utf-8")
        return tap

    def __get_portidx(self):
        port = self.__confxml.findtext(VTAG.XML_TAG_PORTIDX)
        ports = self.__dataxml.get_ports()
        while port in ports:
            port = str(int(port) + 1)
        self.__confxml.find(VTAG.XML_TAG_PORTIDX).text = str(int(port) + 1)
        self.__confxml.write(self.__xml_path, encoding = "utf-8")
        return port

    def __add_ipidx(self, ip, mask = "255.255.255.0"):
        last = 2
        #mlst = mask.split('.', 3)
        #for m in mlst:
        #    if not m == "255":
        #        break
        #    else:
        #        last += 1
        a_list = ip.split('.')
        a_list[3] = '0'
        cry = 1
        for i in range(last, -1, -1):
            val = int(a_list[i]) + cry
            a_list[i] = str(val % 255)
            cry = val // 255

        if not cry == 0:
            return "" 
        return ".".join(a_list) 

    def __get_ipidx(self):
        ip = self.__confxml.findtext(VTAG.XML_TAG_ADDRIDX)
        ips = self.__dataxml.get_ips()
        while ip in ips:
           ip = self.__add_ipidx(ip) 

        if ip is "":
           return ""

        self.__confxml.find(VTAG.XML_TAG_ADDRIDX).text = self.__add_ipidx(ip)
        self.__confxml.write(self.__xml_path, encoding = "utf-8")
        return ip + ' ' + VTAG.IP_MASK8

    #def __add_confidx(self, tap, port, ip):
    #    self.__confxml.find(VTAG.XML_TAG_TAPIDX).text = str(int(tap) + 1)
    #    self.__confxml.find(VTAG.XML_TAG_PORTIDX).text = str(int(port) + 1)
    #    a_list = ip.split('.')
    #    cry = 1
    #    for i in range(2, -1, -1):
    #        val = int(a_list[i]) + cal
    #        a_list[i] = val % 255
    #        cal = val // 255

    #    if not cal == 0:
    #        return False
    #    else:
    #        self.__confxml.find(VTAG.XML_TAG_ADDRIDX).text = ".".join(a_list)
    #        self.__confxml.write(self.__xml_path, encoding = "utf-8")
    #        return True

    def __init_server_conf(self, usr, sev, conf):
        conf_dic = {}
        conf_dic[VTAG.TAG_PROTO] = VTAG.PROTO_UDP
        conf_dic[VTAG.TAG_C2C] = "1"
        conf_dic[VTAG.TAG_KALIVE] = VTAG.TIME_ALIVE
        conf_dic[VTAG.TAG_MAXC] = ";"

        usr_obj = self.__usr_dic[usr]
        usr_dir = usr_obj.get_usr_dir()
        conf_dir = usr_dir + '/' + VTAG.DIR_CONFIG + '/'
        log_dir = usr_dir + '/' + VTAG.DIR_LOG + '/'
        conf_dic[VTAG.TAG_CA] = conf_dir + VTAG.CA_CRT
        conf_dic[VTAG.TAG_CERT] = conf_dir + usr + VTAG.SUF_CRT
        conf_dic[VTAG.TAG_KEY] = conf_dir + usr + VTAG.SUF_KEY
        conf_dic[VTAG.TAG_DH] = conf_dir + VTAG.DH_PEM1
        conf_dic[VTAG.TAG_TLS] = conf_dir + VTAG.TA_KEY

        log_pre = log_dir + sev + '_'
        conf_dic[VTAG.TAG_IPPOOL] = ';'
        conf_dic[VTAG.TAG_STAUS] = log_pre + VTAG.SIGN_STATUS + VTAG.SUF_LOG
        conf_dic[VTAG.TAG_LOG] = log_pre + VTAG.SIGN_LOG + VTAG.SUF_LOG

        for key in conf:
            conf_dic[key] = conf[key]

        #conf_dic[VTAG.TAG_PORT] = conf_dic[VTAG.TAG_DEV] = \
        #conf_dic[VTAG.TAG_CERT] = conf_dic[VTAG.TAG_KEY] = \
        #conf_dic[VTAG.TAG_SERVER] = conf_dic[VTAG.TAG_TLS] = \
        #conf_dic[VTAG.TAG_IPPOOL] = conf_dic[VTAG.TAG_STATUS] = \
        #conf_dic[VTAG.TAG_LOG] = ";"

        return conf_dic

    def __detect_server_conf(self, usr, name, conf):
        # detect name
        if self.__dataxml.is_server_exist(usr, name) or \
            usr_obj.has_server(name):
            self.__log.write_warn("The '%s' server belong to '%s' is in use." % \
                name, usr)
            ## replace the server ...
            return False

        # detect port
        if conf.has_key(VTAG.TAG_PORT):
            if self.__detect_port(conf[VTAG.TAG_PORT]):
                self.__log.write_error("The port is in use.")
                return False

        # detect device
        if conf.has_key(VTAG.TAG_DEV):
            if self.__detect_tap(conf[VTAG.TAG_DEV]):
                self.__log.write_error("The device name is in use.")
                return False

        # detect ip and mask
        if conf.has_key(VTAG.TAG_SERVER):
            server = conf[VTAG.TAG_SERVER].split(' ', 1)
            if self.__detect_ip(server[0], server[1]):
                self.__log.write_error("The ip domain is in use.")
                return False

        return True

    def __set_server_conf(self, usr, name, conf = {}):
        conf_dic = self.__init_server_conf(usr, name, conf)

        if not conf.has_key(VTAG.TAG_PORT):
            port_idx = self.__get_portidx()
            conf_dic[VTAG.TAG_PORT] = port_idx
        else:
            conf_dic[VTAG.TAG_PORT] = conf[VTAG.TAG_PORT]

        if not conf.has_key(VTAG.TAG_DEV):
            tap_idx = self.__get_tapidx()
            conf_dic[VTAG.TAG_DEV] = tap_idx
        else:
            conf_dic[VTAG.TAG_DEV] = conf[VTAG.TAG_DEV]

        if not conf.has_key(VTAG.TAG_SERVER):
            addr_idx = self.__get_ipidx()
            conf_dic[VTAG.TAG_SERVER] = addr_idx
        else:
            ip_mask = conf[VTAG.TAG_SERVER].split(' ')
            ipd = self.__format_ip(ip_mask[0],  ip_mask[1])
            conf_dic[VTAG.TAG_SERVER] = ipd + ' ' + ip_mask[1]

        return conf_dic

    def __add_server(self, usr, conf):
        # add a server according to different config
        if not self.__check_usr(usr):
            return False

        ser_name = self.__confirm_sev_name(usr, conf)
        if ser_name is "":
            return False

        if self.__detect_server_conf(usr, ser_name, conf):
            return False

        usr_obj = self.__usr_dic[usr]
        conf_dic = self.__set_server_conf(usr, ser_name, conf)

        if self.__detect_server_conf(usr, ser_name, conf):
            return False

        usr_obj.vpn_add_server(self.__template, ser_name, conf_dic)
        # add a server for the user in the xml file
        self.__dataxml.xml_add_server(usr, ser_name, conf_dic)

        self.__log.write_ex("Add '%s' server for '%s' successfully." % \
            (ser_name, usr))

        return True

    def __del_server(self, usr, conf):
        pass

    def __manage_server(self):
        sev_list = self.__guide.get_servers()

        for sev in sev_list:
            usr_n = sev[0]
            op_dic = sev[1]
            task = op_dic[VTAG.OPT_TASK]
            
            usr_obj = VSEV(usr_n, self.__vpn_dir + "/z_" + usr_n, self.__log_conf)
            self.__usr_dic[usr_n] = usr_obj
                          
            if task == VTAG.TASK_ADD:
                # add server 
                if not self.__add_server(usr_n, op_dic):
                    return False

            elif task == VTAG.TASK_DEL:
                # del 
                
                pass
            elif task == VTAG.TASK_SEA:
                # search
                pass
            elif task == VTAG.TASK_UP:
                #update
                pass

    def __del_client(self, usr, conf):
        if not conf.has_key(VTAG.OPT_NAME):
            self.__log.write_error(\
                "The client which is being added is lack of name.")
            return False

        self.__usr_dic[usr].vpn_del_client(conf[VTAG.OPT_NAME])

    def __add_client(self, usr, conf):
        usr_obj = self.__usr_dic[usr]
        usr_dir = usr_obj.get_usr_dir()
        if not self.__verify_usr_dir(usr_dir):
            self.__log.write_error(\
                "Invalid user directory for the adding client.")
            return False

        if not conf.has_key(VTAG.OPT_NAME):
            self.__log.write_error(\
                "The client which is being added is lack of name.")
            return False

        if usr_obj.has_client(conf[VTAG.OPT_NAME]):
            self.__log.write_warn( "The client '%s' has already been used." % \
                conf[VTAG.OPT_NAME])
            flag = raw_input("Are you sure to replace it![y/n]: ")
            if not flag == 'y':
                return True
            else:
                usr_obj.vpn_del_client(conf[VTAG.OPT_NAME])

        if not usr_obj.vpn_add_client(name = conf[VTAG.OPT_NAME]):
            self.__log.write_error("Fail to add '%s' client certification." % \
                conf[VTAG.OPT_NAME])
            return False
     
        self.__log.write_ex("Add '%s' client certification for '%s' successfully." % \
            (conf[VTAG.OPT_NAME], usr))

        return True

    def __manage_client(self):
        clt_list = self.__guide.get_clients()

        for usr_n, op_dic in clt_list:
            task = op_dic[VTAG.OPT_TASK]

            if task == VTAG.TASK_ADD:
                # add client
                if not self.__add_client(self, usr_n, op_dic):
                    return False

            elif task == VTAG.TASK_DEL:
                # del 
                pass
            elif task == VTAG.TASK_SEA:
                # search
                pass
            elif task == VTAG.TASK_UP:
                #update
                pass
            pass

       
    def __args_default(self, fs = True, fc = True):

        if fs:
            if not self.__manage_server():
                return False

        if fc:
            if not self.__manage_client():
                return False

        return True

    def __vars(self):
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
            print "[ERROR]: Lack of server template file."
            return False
        self.__dxml_path = self.__confxml.findtext(VTAG.XML_TAG_DATAXML)
        self.__dataxml = VXML(self.__dxml_path)
        if not os.path.isfile(self.__dxml_path):
            self.__dataxml.xml_create() 


        if not self.__ARG_CONF in arg_dic:
            self.__guide_path = self.__confxml.findtext(VTAG.XML_TAG_GUIDE)
        else:
            self.__guide_path = self.__args[self.__ARG_CONF]
        if not os.path.isfile(self.__guide_path):
            self.__log.write_error("Lack of guide config file.")
            return False
        self.__guide = VGP(self.__guide_path)

        return True


    def show_usage(self):
        """
        Show usage
        """
        
        print """VPN Deploy Script.
        General Options:
        -h, --help      : Show options.
        --conf=file     : Read configuration options from file.
        """
        
    def parse_argv(self):
        """
        Parse arguments
        """
        args_str = "hcs"
        args_list = ["help", "conf="]
        opt, args = getopt.getopt(self.__argv[1:], args_str, args_list)

        for op, arg in opt:
            if op == "-h" or op == "--help":
                self.show_usage()
                return True
            if op == "--conf":
                self.__args[op] = arg
            if op == "-s":
                self.__args[op] = ''
            if op == "-c":
                self.__args[op] = ''
        
        if not self.__vars():
            return False

        return True

    def excute(self):
        """
        Excute operations 
        """
        if not self.parse_argv():
            return

        #if not self.__args:
        #    self.__args_default()
        #    return

        #if "-s" in self.__args:
        #    flag_c = False
        #if "-c" in self.__args:
        #    flag_s = False

        #self.__args_default(flag_s, flag_c)
            
if __name__ == "__main__":

    VpnDeploy(sys.argv).excute()

    import re
    strsss = "a  b  x  "
    list = re.split("\s+", strsss.strip())
    print list
    print len(list)

    l2 = [("a", "bs"), ("b", "cs")]
    if ('a', 'bs') in l2:
        print "include"

    ls2 = ['1','2','3']
    print '.'.join(ls2)

    dic = {}
    dic["1"] = 1
    pass