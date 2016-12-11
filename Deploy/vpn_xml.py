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
    __TAG_SEVCNT = "servercnt"
    __TAG_VDIR = "vpn_dir"
    __TAG_GUIDE = "guide"
    __TAG_USER = "user"
    __TAG_SEVIDX = "serveridx"
    __TAG_SCNT = "scnt"
    __TAG_KEYSDIR = "keys_dir"
    __TAG_CONFIGDIR = "config_dir"
    __TAG_LOGDIR = "log_dir"
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

    def __get_usr(self, usr):
        ptn = self.__TAG_USER + "[@" + self.__ATTR_N + '="' + usr + '"]'
        return self.__xml_parse().find(ptn)

    def get_usr_sevidx(self, usr):
        """
        Get the index of new server of the user
        @usr: user name
        """
        return int(self.__get_usr(usr).findtext(self.__TAG_SEVIDX))

    def is_usr_exist(self, usr):
        """
        Detect if the usr existed
        @usr: user name
        """
        return (True if self.__get_usr(usr) is not None else False)

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
        for ele in self.__root.findall(self.__TAG_USER):
            if ele.attrib[self.__ATTR_N] == usr:
                self.__root.remove(ele)
                break

        tcnt = self.__root.find(self.__TAG_TENCNT)
        tcnt.text = str(int(tcnt.text) - 1)
        self.xml_write()

    def xml_add_server(self, usr, name, conf):
        """
        Add a user server information into xml file
        @usr: user name
        @name: server name
        @conf: server config dictionary
        """
        


    def xml_write(self):
        """
        Write new content into xml file
        """
        self.__tree.write(self.__path, encoding = "utf-8", xml_declaration="true")




if __name__ == "__main__":
    path = "./test.txt"
    tree = ET.parse(path)