#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import re
from vpn_file import VpnFile
from vpn_tag import VpnTag

class VpnConf(VpnFile):
    """
    OpenVPN server config
    """

    # self const vars
    #TAG_PORT = "port"
    #TAG_PROTO = "proto"
    #TAG_DEV = "dev"
    #TAG_CA = "ca"
    #TAG_CERT = "cert"
    #TAG_KEY = "key"
    #TAG_DH = "dh"
    #TAG_SERVER = "server"
    #TAG_IPPOOL = "ifconfig-pool-persist"
    #TAG_C2C = "client-to-client"
    #TAG_KALIVE = "keepalive"
    #TAG_TLS = "tls-auth"
    #TAG_MAXC = "max-clients"
    #TAG_STATUS = "status"
    #TAG_LOG = "log"
    _TAG_MARK = " ..."

    # self._re_dic: regular dictionary
    # self._val_dic: value dictionary
    # self._old_dic: file value dictionary
    
    
    def __init__(self, path):
        super(VpnConf, self).__init__(path)

        self._re_dic = {\
            VpnTag.TAG_PORT:r"(^port [\S|\s]*?$)", \
            VpnTag.TAG_PROTO:r"(^proto [\S|\s]*?$)", \
            VpnTag.TAG_DEV:r"(^dev [\S|\s]*?$)", \
            VpnTag.TAG_CA:r"(^ca [\S|\s]*?$)", \
            VpnTag.TAG_CERT:r"(^cert [\S|\s]*?$)", \
            VpnTag.TAG_KEY:r"(^key [\S|\s]*?$)", \
            VpnTag.TAG_DH:r"(^dh [\S|\s]*?$)", \
            VpnTag.TAG_SERVER:r"(^server [\S|\s]*?$)", \
            VpnTag.TAG_IPPOOL:r"(^[#;]*ifconfig\-pool\-persist [\S|\s]*?$)", \
            VpnTag.TAG_C2C:r"(^[#;]*client\-to\-client[\S|\s]*?$)", \
            VpnTag.TAG_KALIVE:r"(^keepalive [\S|\s]*?$)", \
            VpnTag.TAG_TLS:r"(^tls\-auth [\S|\s]*?$)", \
            VpnTag.TAG_MAXC:r"(^[#;]*max\-clients [\S|\s]*?$)", \
            VpnTag.TAG_STATUS:r"(^[#;]*status [\S|\s]*?$)", \
            VpnTag.TAG_LOG:r"(^[#;]*log [\S|\s]*?$)"}
        self._val_dic = {\
            VpnTag.TAG_PORT:"", \
            VpnTag.TAG_PROTO:"", \
            VpnTag.TAG_DEV:"", \
            VpnTag.TAG_CA:"", \
            VpnTag.TAG_CERT:"", \
            VpnTag.TAG_KEY:"", \
            VpnTag.TAG_DH:"", \
            VpnTag.TAG_SERVER:"", \
            VpnTag.TAG_IPPOOL:"", \
            VpnTag.TAG_C2C:"", \
            VpnTag.TAG_KALIVE:"", \
            VpnTag.TAG_TLS:"", \
            VpnTag.TAG_MAXC:"", \
            VpnTag.TAG_STATUS:"", \
            VpnTag.TAG_LOG:""}
        self._old_dic = {\
            VpnTag.TAG_PORT:"", \
            VpnTag.TAG_PROTO:"", \
            VpnTag.TAG_DEV:"", \
            VpnTag.TAG_CA:"", \
            VpnTag.TAG_CERT:"", \
            VpnTag.TAG_KEY:"", \
            VpnTag.TAG_DH:"", \
            VpnTag.TAG_SERVER:"", \
            VpnTag.TAG_IPPOOL:"", \
            VpnTag.TAG_C2C:"", \
            VpnTag.TAG_KALIVE:"", \
            VpnTag.TAG_TLS:"", \
            VpnTag.TAG_MAXC:"", \
            VpnTag.TAG_STATUS:"", \
            VpnTag.TAG_LOG:""}

    def _var_clear(self):
        for key in self._val_dic:
            self._val_dic[key] = ""

    def __pack_value(self, tag, attr):
        val = tag
        if ('#' or ';') in attr:
            val = ';' + val + ' '
            return val

        if tag == VpnTag.TAG_C2C:
            if attr == '1':
                return val
            return ';' + val
                       
        val = tag + ' ' + attr
        return val

    def __get_option(self, tag):
        conf_file = open(self._path, 'r')
        context = conf_file.readlines()
        conf_file.close()

        for line in context:
            if re.match(self._re_dic[tag], line):
                if tag == self._TAG_C2C:
                    if line[0] == 'c':
                        return '1'
                    else:
                        return '0'
                if line[0] == '#' or line[0] == ';':
                    return ""
                return line.strip('\n').split(' ', 1)[1]

    def get_conf_options(self):
        """
        Get current options in the config file 
        @return: options dictionary of the config file
        """
        conf_file = open(self._path, 'r')
        context = conf_file.readlines()
        conf_file.close()

        for line in context:
            for key in self._re_dic:
                if re.match(self._re_dic[key], line):
                    #if key == self._TAG_C2C:
                    #    if line[0] == 'c':
                    #        self._val_dic[key] = '1'
                    #    continue
                    #if not (line[0] == '#' or line[0] == ';'):
                    self._old_dic[key] = line.strip('\n')

        return self._old_dic
    
    def conf_flush(self):
        """
        Write modified options into the config file
        """
        conf_file = open(self._path, 'r')
        context = conf_file.read()
        conf_file.close()

        for key in self._val_dic:
            if not self._val_dic[key] == "":
                attr = self.__pack_value(key, self._val_dic[key])
                context = re.sub(self._re_dic[key], attr, context, 1, re.M)

        conf_file = open(self._path, 'w')
        conf_file.write(context)
        conf_file.close()

    def set_port(self, port):
        """
        Set the port number in the file
        """
        self.set_port_var(port)
        port = self.__pack_value(VpnTag.TAG_PORT, port)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_PORT], port)

    def set_port_var(self, port):
        """
        Set the port variable
        """
        self._val_dic[VpnTag.TAG_PORT] = port

    def get_port(self):
        """
        Get the port number
        """
        return self._val_dic[VpnTag.TAG_PORT]

    def set_proto(self, proto):
        """
        Set the protocal type in the file
        """
        self.set_proto_var(proto)
        proto = self.__pack_value(VpnTag.TAG_PROTO, proto)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_PROTO], proto)

    def set_proto_var(self, proto):
        """
        Set the protocal variable
        """
        self._val_dic[VpnTag.TAG_PROTO] = proto

    def get_proto(self):
        """
        Get the protocal type
        """
        return self._val_dic[VpnTag.TAG_PROTO]
    
    def set_dev(self, dev):
        """
        Set the device in the file
        """
        self.set_dev_var(dev)
        dev = self.__pack_value(VpnTag.TAG_DEV, dev)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_DEV], dev)

    def set_dev_var(self, dev):
        """
        Set the device variable
        """
        self._val_dic[VpnTag.TAG_DEV] = dev

    def get_dev(self):
        """
        Get the device 
        """
        return self._val_dic[VpnTag.TAG_DEV]

    def set_ca(self, ca):
        """
        Set the ca certificate in the file
        """
        self.set_ca_var(ca)
        ca = self.__pack_value(VpnTag.TAG_CA, CA)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_CA], ca)

    def set_ca_var(self, ca):
        """
        Set the ca certificate variable
        """
        self._val_dic[VpnTag.TAG_CA] = ca

    def get_ca(self):
        """
        Get the ca certificate 
        """
        return self._val_dic[VpnTag.TAG_CA]

    def set_cert(self, cert):
        """
        Set the server certificertte in the file
        """
        self.set_cert_var(cert)
        cert = self.__pack_value(VpnTag.TAG_CERT, cert)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_CERT], cert)

    def set_cert_var(self, cert):
        """
        Set the server certificertte variable
        """
        self._val_dic[VpnTag.TAG_CERT] = cert

    def get_cert(self):
        """
        Get the server certificertte 
        """
        return self._val_dic[VpnTag.TAG_CERT]

    def set_key(self, key):
        """
        Set the server key in the file
        """
        self.set_key_var(key)
        key = self.__pack_value(VpnTag.TAG_KEY, key)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_KEY], key)

    def set_key_var(self, key):
        """
        Set the server key variable
        """
        self._val_dic[VpnTag.TAG_KEY] = key

    def get_key(self):
        """
        Get the server key 
        """
        return self._val_dic[VpnTag.TAG_KEY]

    def set_dh(self, dh):
        """
        Set the server dh in the file
        """
        self.set_dh_var(dh)
        dh = self.__pack_value(VpnTag.TAG_DH, dh)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_DH], dh)

    def set_dh_var(self, dh):
        """
        Set the server dh variable
        """
        self._val_dic[VpnTag.TAG_DH] = dh

    def get_dh(self):
        """
        Get the server dh 
        """
        return self._val_dic[VpnTag.TAG_DH]

    def set_server(self, server):
        """
        Set the vpn ip range in the file
        """
        self.set_server_var(server)
        server = self.__pack_value(VpnTag.TAG_SERVER, server)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_SERVER], server)

    def set_server_var(self, server):
        """
        Set the vpn ip range variable
        """
        self._val_dic[VpnTag.TAG_SERVER] = server

    def get_server(self):
        """
        Get the vpn ip range
        """
        return self._val_dic[VpnTag.TAG_SERVER]

    def set_ippool(self, ippool):
        """
        Set the ifconfig-pool-persist in the file
        """
        self.set_ippool_var(ippool)
        ippool = self.__pack_value(VpnTag.TAG_IPPOOL, ippool)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_IPPOOL], ippool)

    def set_ippool_var(self, ippool):
        """
        Set the ifconfig-pool-persist variable
        """
        self._val_dic[VpnTag.TAG_IPPOOL] = ippool

    def get_ippool(self):
        """
        Get the ifconfig-pool-persist
        """
        return self._val_dic[VpnTag.TAG_IPPOOL]

    def set_c2c(self, c2c):
        """
        Set the client-to-client in the file
        """
        self.set_c2c_var(c2c)
        c2c = self.__pack_value(VpnTag.TAG_C2C, c2c)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_C2C], c2c)

    def set_c2c_var(self, c2c):
        """
        Set the client-to-client variable
        """
        self._val_dic[VpnTag.TAG_C2C] = c2c

    def get_c2c(self):
        """
        Get the client-to-client
        """
        return self._val_dic[VpnTag.TAG_C2C]

    def set_kalive(self, kalive):
        """
        Set the keepalive in the file
        """
        self.set_kalive_var(kalive)
        kalive = self.__pack_value(VpnTag.TAG_KALIVE, kalive)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_KALIVE], kalive)

    def set_kalive_var(self, kalive):
        """
        Set the keepalive variable
        """
        self._val_dic[VpnTag.TAG_KALIVE] = kalive

    def get_kalive(self):
        """
        Get the keepalive
        """
        return self._val_dic[VpnTag.TAG_KALIVE]

    def set_tls(self, tls):
        """
        Set the tls-auth in the file
        """
        self.set_tls_var(tls)
        tls = self.__pack_value(VpnTag.TAG_TLS, tls)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_TLS], tls)

    def set_tls_var(self, tls):
        """
        Set the tls-auth variable
        """
        self._val_dic[VpnTag.TAG_TLS] = tls

    def get_tls(self):
        """
        Get the tls-auth
        """
        return self._val_dic[VpnTag.TAG_TLS]
    
    def set_maxc(self, maxc):
        """
        Set the max-clients in the file
        """
        self.set_maxc_var(maxc)
        maxc = self.__pack_value(VpnTag.TAG_MAXC, maxc)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_MAXC], maxc)

    def set_maxc_var(self, maxc):
        """
        Set the max-clients variable
        """
        self._val_dic[VpnTag.TAG_MAXC] = maxc

    def get_maxc(self):
        """
        Get the max-clients
        """
        return self._val_dic[VpnTag.TAG_MAXC]

    def set_status(self, status):
        """
        Set the status log in the file
        """
        self.set_status_var(status)
        status = self.__pack_value(VpnTag.TAG_STATUS, status)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_STATUS], status)

    def set_status_var(self, status):
        """
        Set the status log variable
        """
        self._val_dic[VpnTag.TAG_STATUS] = status

    def get_status(self):
        """
        Get the status log
        """
        return self._val_dic[VpnTag.TAG_STATUS]

    def set_log(self, log):
        """
        Set the log in the file
        """
        self.set_log_var(log)
        log = self.__pack_value(VpnTag.TAG_LOG, log)
        self.vpn_line_update_re(self._re_dic[VpnTag.TAG_LOG], log)

    def set_log_var(self, log):
        """
        Set the log variable
        """
        self._val_dic[VpnTag.TAG_LOG] = log

    def get_log(self):
        """
        Get the log
        """
        return self._val_dic[VpnTag.TAG_LOG]


if __name__ == "__main__":
    
    vpn_conf = VpnConf("./Resource/server2.conf")
    #print vpn_conf.get_conf_options()
    #vpn_conf.set_port("port 1776")
    #vpn_conf.set_c2c("#client-to-client")
    #vpn_conf.set_status(r"status E:\\vpn\\log\\status.log")
    #vpn_conf.conf_flush()
    str = "log >>>"
    print re.sub("^log", "log E:\\\\vpn", str, 1, re.M)
    print re.sub("^log", "log E:\npn", str, 1, re.M)
    print vpn_conf.is_exist()



