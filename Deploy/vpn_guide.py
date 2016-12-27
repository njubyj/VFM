#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser as CP
from vpn_tag import VpnTag

class VpnGuideParser(object):
    """
    Openvpn guide config parser
    """

    # self.__path: guide config file path
    # self.__conf: ConfigParser for guide config

    def __init__(self, path):
        self.__path = path
        self.__conf = CP.ConfigParser()
        self.__conf.read(self.__path)

    def __get_options(self):
        if not self.__conf.has_section(VpnTag.SEC_OPTIONS):
            return [] 
        
        return self.__conf.get(VpnTag.SEC_OPTIONS, \
            VpnTag.OPT_KEYS).split(',')

    def __is_server(self):
        if VpnTag.SEC_SERVER in self.__get_options():
            return True
        else:
            return False

    def __is_client(self):
        if VpnTag.SEC_CLIENT in self.__get_options():
            return True
        else:
            return False

    def __parse_server_sec(self, sec):
        empty = ()
        val_dic = {}

        ops = self.__conf.options(sec)
        if VpnTag.OPT_USR in ops:
            usr = self.__conf.get(sec, VpnTag.OPT_USR)
            if not usr:
                return empty
            val_dic[VpnTag.OPT_TASK] = VpnTag.TASK_ADD
        else:
            return empty

        #if (len(ops) == 1 and ops[0] == self.__OPT_USR) or \
        #   (not ops):
        #    return sec_dic

        for op in ops:
            if (op == VpnTag.OPT_TASK) and \
               (self.__conf.get(sec,op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.OPT_NAME) and \
               (self.__conf.get(sec,op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_PORT) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_PROTO) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_DEV) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_CA) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_CERT) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_KEY) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_DH) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_SERVER) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_IPPOOL) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_C2C) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_KALIVE) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_TLS) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_MAXC) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_STATUS) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.TAG_LOG) and \
               (self.__conf.get(sec, op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue

        return (usr, val_dic)

    def __parse_client_sec(self, sec):
        empty = ()
        val_dic = {}

        ops = self.__conf.options(sec)
        if VpnTag.OPT_USR in ops:
            usr = self.__conf.get(sec, VpnTag.OPT_USR)
            if not usr:
                return empty
            val_dic[VpnTag.OPT_TASK] = VpnTag.TASK_ADD
        else:
            return empty

        for op in ops:
            if (op == VpnTag.OPT_TASK) and \
               (self.__conf.get(sec,op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue
            if (op == VpnTag.OPT_NAME) and \
               (self.__conf.get(sec,op)):
                val_dic[op] = self.__conf.get(sec, op)
                continue

        return (usr, val_dic)

    def get_servers(self):
        """
        Get server list
        """
        sev_list = []
        sev_secs = []
        
        if not self.__is_server():
            return sev_list

        if (not self.__conf.has_section(VpnTag.SEC_SERVER)) or \
           (not self.__conf.has_option(VpnTag.SEC_SERVER, \
                                       VpnTag.OPT_KEYS)):
            return sev_list

        keys = self.__conf.get(VpnTag.SEC_SERVER, VpnTag.OPT_KEYS)
        if keys == "":
            return sev_list
        keys = keys.split(',')

        for key in keys:
            sev_secs.append(VpnTag.SEC_SERVER + '_' + key)

        for sec in sev_secs:
            if self.__conf.has_section(sec):
                sev_tup = self.__parse_server_sec(sec)
                if sev_tup:
                    sev_list.append(sev_tup)

        return sev_list

    def get_clients(self):
        """
        Get client list
        """
        clt_list = []
        clt_secs = []

        if not self.__is_client():
            return clt_list

        if (not self.__conf.has_section(VpnTag.SEC_CLIENT)) or \
           (not self.__conf.has_option(VpnTag.SEC_CLIENT, \
                                       VpnTag.OPT_KEYS)):
            return clt_list

        keys = self.__conf.get(VpnTag.SEC_CLIENT, VpnTag.OPT_KEYS)
        if keys == "":
            return clt_list
        keys = keys.split(',')

        for key in keys:
            clt_secs.append(VpnTag.SEC_CLIENT + '_' + key)

        for sec in clt_secs:
            if self.__conf.has_section(sec):
                clt_tup = self.__parse_client_sec(sec)
                if clt_tup:
                    clt_list.append(clt_tup)

        return clt_list

                
if __name__ == "__main__":
    conf = CP.ConfigParser()
    conf.read(".\\Resource\\VPN.conf")

    print conf.options("server_1")