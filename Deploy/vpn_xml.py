#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import os
import xml.etree.ElementTree as ET
from vpn_tag import VpnTag as VTAG

class VpnXml(object):
    """
    Vpn 'xml' file manager
    """
    __TAG_VPN = "openvpn"
    __TAG_TENCNT = "tenantcnt"
    __TAG_SEVCNT = "servertotal"
    __TAG_VDIR = "vpn_dir"
    __TAG_GUIDE = "guide"
    __TAG_USER = "user"
    __TAG_SEVIDX = "serveridx"
    __TAG_SCNT = "scnt"
    __TAG_KEYSDIR = "keys_dir"
    __TAG_CONFIGDIR = "config_dir"
    __TAG_LOGDIR = "log_dir"
    __TAG_SERVER = "server"
    __TAG_PORT = "port"
    __TAG_PROTO = "proto"
    __TAG_DEV = "dev"
    __TAG_IPS = "ips"
    __TAG_MASK = "mask"
    __TAG_ALIVE = "alive"
    __TAG_MAX = "max"
    __TAG_C2C = "ctoc"
    __TAG_FTP = "ftpinfo"
    __TAG_KEYSCONF = "keysconf"
    __TAG_CA = "ca"
    __TAG_DH = "dh"
    __TAG_TLS = "tls"
    __TAG_CERT = "cert"
    __TAG_KEY = "key"
    __TAG_LOGMSG = "logmsg"
    __TAG_IPP = "ippool"
    __TAG_LOG = "log"
    __TAG_STATUS = "staus"
    __TAG_PID = "pid"
    __ATTR_ID = "id"
    __ATTR_N = "n"
    __ATTR_DIR = "dir"


    def __init__(self, path):
        self.__path = path

    def __xml_parse(self):
        self.__tree = ET.parse(self.__path)
        root = self.__tree.getroot()
        return root

    def __add_tenantcnt(self):
        """
        Add 'tenantcnt' element
        """
        if self.__root.find(self.__TAG_TENCNT) is None:
            tcnt = ET.Element(self.__TAG_TENCNT)
            tcnt.text = "0"
            self.__root.append(tcnt)

    def __add_servercnt(self):
        """
        Add 'servercnt' element
        """
        if self.__root.find(self.__TAG_SEVCNT) is None:
            scnt = ET.Element(self.__TAG_SEVCNT)
            scnt.text = "0"
            self.__root.append(scnt)

    def xml_create(self):
        """
        Create a new xml file
        """
        if not os.path.isfile(self.__path):
            self.__root = ET.Element(self.__TAG_VPN)
            self.__tree = ET.ElementTree(self.__root)
            self.__add_tenantcnt()
            self.__add_servercnt()
            self.xml_write()

    def get_user_cnt(self):
        """
        Get the number of user 
        """
        return int(self.__xml_parse().findtext(self.__TAG_TENCNT))

    def get_server_cnt(self):
        """
        Get the number of server
        """
        return int(self.__xml_parse().findtext(self.__TAG_SEVCNT))

    def __get_usr(self, usr, root):
        ptn = self.__TAG_USER + "[@" + self.__ATTR_N + '="' + usr + '"]'
        return root.find(ptn)

    def is_usr_exist(self, usr):
        """
        Detect if the usr existed
        @usr: user name
        """
        root = self.__xml_parse()
        return (True if self.__get_usr(usr, root) is not None else False)

    def get_usr_sevidx(self, usr):
        """
        Get the index of new server of the user
        @usr: user name
        """
        root = self.__xml_parse()
        if self.__get_usr(usr, root) is None:
            return None
        return int(self.__get_usr(usr, root).findtext(self.__TAG_SEVIDX))
    
    def get_usr_sevcnt(self, usr):
        """
        Get the number of servers of the user
        @usr: user name
        """
        root = self.__xml_parse()
        if self.__get_usr(usr, root) is None:
            return None
        return int(self.__get_usr(usr, root).findtext(self.__TAG_SCNT))

    def xml_add_usr(self, usr, id, dir):
        """
        Add a user information into xml file
        @usr: user name
        @id: user index
        @dir: user directory
        """
        self.__root = self.__xml_parse()
        attr_dic = {}
        attr_dic[self.__ATTR_ID] = id
        attr_dic[self.__ATTR_N] = usr
        attr_dic[self.__ATTR_DIR] = dir
        keys_dir = dir + '/' + VTAG.DIR_KEYS
        config_dir = dir + '/' + VTAG.DIR_CONFIG
        log_dir = dir + '/' + VTAG.DIR_LOG

        usr_ele = ET.Element(self.__TAG_USER, attr_dic)
        seridx_ele = ET.Element(self.__TAG_SEVIDX)
        seridx_ele.text = '1'
        scnt_ele = ET.Element(self.__TAG_SCNT)
        scnt_ele.text = '0'
        keydir_ele = ET.Element(self.__TAG_KEYSDIR)
        keydir_ele.text = keys_dir
        configdir_ele = ET.Element(self.__TAG_CONFIGDIR)
        configdir_ele.text = config_dir
        logdir_ele = ET.Element(self.__TAG_LOGDIR)
        logdir_ele.text = log_dir
        usr_ele.append(seridx_ele)
        usr_ele.append(scnt_ele)
        usr_ele.append(keydir_ele)
        usr_ele.append(configdir_ele)
        usr_ele.append(logdir_ele)
        
        tcnt = self.__root.find(self.__TAG_TENCNT)
        tcnt.text = str(int(tcnt.text) + 1)
        self.__root.append(usr_ele) 
        self.xml_write()

    def xml_del_usr(self, usr):
        """
        Delete the usr element from xml file
        @usr: user name
        """
        self.__root = self.__xml_parse()
        if self.__get_usr(usr, self.__root) is None:
            return
        for ele in self.__root.findall(self.__TAG_USER):
            if ele.attrib[self.__ATTR_N] == usr:
                self.__root.remove(ele)
                break

        tcnt = self.__root.find(self.__TAG_TENCNT)
        tcnt.text = str(int(tcnt.text) - 1)
        self.xml_write()

    def is_server_exist(self, usr, server):
        """
        Detect if the server of the user exists
        @usr: user name
        @server: server name
        """
        if not self.is_usr_exist(usr):
            return False

        root = self.__xml_parse()
        ptn = self.__TAG_SERVER + "[@" + self.__ATTR_N + '="' + server + '"]' 
        if self.__get_usr(usr, root).find(ptn) is not None:
            return True
        else:
            return False

    def __pack_value(self, tag, attr):
        val = ""
        if ('#' in attr) or (';' in attr):
            return val

        val = attr

        if tag == VTAG.TAG_C2C:
            if attr == '1':
                val = '1'
            else:
                val = '0'
        elif tag == VTAG.TAG_CA or \
             tag == VTAG.TAG_CERT or \
             tag == VTAG.TAG_KEY or \
             tag == VTAG.TAG_DH or \
             tag == VTAG.TAG_TLS or \
             tag == VTAG.TAG_LOG or \
             tag == VTAG.TAG_IPPOOL or \
             tag == VTAG.TAG_STATUS:
            val = attr.rsplit('/', 1)[1]

        return val

    def xml_add_server(self, usr, name, conf):
        """
        Add a user server information into xml file
        @usr: user name
        @name: server name
        @conf: server config dictionary
        """
        self.__root = self.__xml_parse()
        usr_ele = self.__get_usr(usr, self.__root)
        id = usr_ele.findtext(self.__TAG_SEVIDX)
        attr_dic = {}
        attr_dic[self.__ATTR_ID] = id
        attr_dic[self.__ATTR_N] = name

        sev_ele = ET.Element(self.__TAG_SERVER, attr_dic)
        port_ele = ET.Element(self.__TAG_PORT)
        port_ele.text = self.__pack_value(VTAG.TAG_PORT, conf[VTAG.TAG_PORT])
        proto_ele = ET.Element(self.__TAG_PROTO)
        proto_ele.text = self.__pack_value(VTAG.TAG_PROTO, conf[VTAG.TAG_PROTO])
        dev_ele = ET.Element(self.__TAG_DEV)
        dev_ele.text = self.__pack_value(VTAG.TAG_DEV, conf[VTAG.TAG_DEV])
        ips_ele = ET.Element(self.__TAG_IPS)
        mask_ele = ET.Element(self.__TAG_MASK)
        val = self.__pack_value(VTAG.TAG_SERVER, conf[VTAG.TAG_SERVER])
        if val:
            ips_ele.text = val.split(' ', 1)[0].strip()
            mask_ele.text = val.split(' ', 1)[1].strip()
        else:
            mask_ele.text = ips_ele.text = ""
        alive_ele = ET.Element(self.__TAG_ALIVE)
        alive_ele.text = self.__pack_value(VTAG.TAG_KALIVE, conf[VTAG.TAG_KALIVE])
        max_ele = ET.Element(self.__TAG_MAX)
        max_ele.text = self.__pack_value(VTAG.TAG_MAXC, conf[VTAG.TAG_MAXC])
        ctoc_ele = ET.Element(self.__TAG_C2C)
        ctoc_ele.text = self.__pack_value(VTAG.TAG_C2C, conf[VTAG.TAG_C2C])
        keyconf_ele = ET.Element(self.__TAG_KEYSCONF)
        ca_ele = ET.Element(self.__TAG_CA)
        ca_ele.text = self.__pack_value(VTAG.TAG_CA, conf[VTAG.TAG_CA])
        dh_ele = ET.Element(self.__TAG_DH)
        dh_ele.text = self.__pack_value(VTAG.TAG_DH, conf[VTAG.TAG_DH])
        tls_ele = ET.Element(self.__TAG_TLS)
        tls_ele.text = self.__pack_value(VTAG.TAG_TLS, conf[VTAG.TAG_TLS])
        cert_ele = ET.Element(self.__TAG_CERT)
        cert_ele.text = self.__pack_value(VTAG.TAG_CERT, conf[VTAG.TAG_CERT])
        key_ele = ET.Element(self.__TAG_KEY)
        key_ele.text = self.__pack_value(VTAG.TAG_KEY, conf[VTAG.TAG_KEY])
        keyconf_ele.append(ca_ele)
        keyconf_ele.append(dh_ele)
        keyconf_ele.append(tls_ele)
        keyconf_ele.append(cert_ele)
        keyconf_ele.append(key_ele)
        logmsg_ele = ET.Element(self.__TAG_LOGMSG)
        ippool_ele = ET.Element(self.__TAG_IPP)
        ippool_ele.text = self.__pack_value(VTAG.TAG_IPPOOL, conf[VTAG.TAG_IPPOOL])
        log_ele = ET.Element(self.__TAG_LOG)
        log_ele.text = self.__pack_value(VTAG.TAG_LOG, conf[VTAG.TAG_LOG])
        status_ele = ET.Element(self.__TAG_STATUS)
        status_ele.text = self.__pack_value(VTAG.TAG_STATUS, conf[VTAG.TAG_STATUS])
        pid_ele = ET.Element(self.__TAG_PID)
        pid_ele.text = name + VTAG.SUF_PID
        logmsg_ele.append(ippool_ele)
        logmsg_ele.append(log_ele)
        logmsg_ele.append(status_ele)
        logmsg_ele.append(pid_ele)

        sev_ele.append(port_ele)
        sev_ele.append(proto_ele)
        sev_ele.append(dev_ele)
        sev_ele.append(ips_ele)
        sev_ele.append(mask_ele)
        sev_ele.append(alive_ele)
        sev_ele.append(max_ele)
        sev_ele.append(ctoc_ele)
        sev_ele.append(keyconf_ele)
        sev_ele.append(logmsg_ele)
        usr_ele.append(sev_ele)

        usr_ele.find(self.__TAG_SEVIDX).text = str(int(id) + 1)
        scnt_ele = usr_ele.find(self.__TAG_SCNT)
        scnt_ele.text = str(int(scnt_ele.text) + 1)
        sevcnt_ele = self.__root.find(self.__TAG_SEVCNT)
        sevcnt_ele.text = str(int(sevcnt_ele.text) + 1)

        self.xml_write()

    def xml_del_server(self, usr, name):
        """
        Delete a user server element 
        @usr: user name
        @name: server name
        """
        self.__root = self.__xml_parse()
        usr_ele = self.__get_usr(usr, self.__root)
        if usr_ele is not None:
            for sev in usr_ele.findall(self.__TAG_SERVER):
                if sev.attrib[self.__ATTR_N] == name:
                    usr_ele.remove(sev)
                    scnt = usr_ele.find(self.__TAG_SCNT)
                    scnt.text = str(int(scnt.text) - 1)
                    break

            sevcnt = self.__root.find(self.__TAG_SEVCNT)
            sevcnt.text = str(int(sevcnt.text) - 1)
            self.xml_write()

    def xml_write(self):
        """
        Write new content into xml file
        """
        self.__tree.write(self.__path, encoding = "utf-8", xml_declaration="true")




if __name__ == "__main__":
    path = "./test.txt"
    tree = ET.parse(path)