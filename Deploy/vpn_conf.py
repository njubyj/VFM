#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import re
from vpn_file import VpnFile

class VpnConf(VpnFile):
    """
    OpenVPN server config
    """

    # self const vars
    _TAG_PORT = "port"
    _TAG_PROTO = "proto"
    _TAG_DEV = "dev"
    _TAG_CA = "ca"
    _TAG_CERT = "cert"
    _TAG_KEY = "key"
    _TAG_DH = "dh"
    _TAG_SERVER = "server"
    _TAG_IPPOOL = "ifconfig-pool-persist"
    _TAG_C2C = "client-to-client"
    _TAG_KALIVE = "keepalive"
    _TAG_TLS = "tls-auth"
    _TAG_MAXC = "max-clients"
    _TAG_STAUS = "status"
    _TAG_LOG = "log"
    _TAG_MARK = " ..."

    # self._re_dic: regular dictionary
    # self._val_dic: value dictionary
    
    
    def __init__(self, path):
        super(VpnConf, self).__init__(path)

        self._re_dic = {\
            self._TAG_PORT:r"(^port [\S|\s]*?$)", \
            self._TAG_PROTO:r"(^proto [\S|\s]*?$)", \
            self._TAG_DEV:r"(^dev [\S|\s]*?$)", \
            self._TAG_CA:r"(^ca [\S|\s]*?$)", \
            self._TAG_CERT:r"(^cert [\S|\s]*?$)", \
            self._TAG_KEY:r"(^key [\S|\s]*?$)", \
            self._TAG_DH:r"(^dh [\S|\s]*?$)", \
            self._TAG_SERVER:r"(^server [\S|\s]*?$)", \
            self._TAG_IPPOOL:r"(^[#;]*ifconfig\-pool\-persist[\S|\s]*?$)", \
            self._TAG_C2C:r"(^[#;]*client\-to\-client[\S|\s]*?$)", \
            self._TAG_KALIVE:r"(^keepalive [\S|\s]*?$)", \
            self._TAG_TLS:r"(^tls\-auth [\S|\s]*?$)", \
            self._TAG_MAXC:r"(^[#;]*max\-clients [\S|\s]*?$)", \
            self._TAG_STAUS:r"(^[#;]*status[\S|\s]*?$)", \
            self._TAG_LOG:r"(^[#;]*log[\S|\s]*?$)"}
        self._val_dic = {\
            self._TAG_PORT:"", \
            self._TAG_PROTO:"", \
            self._TAG_DEV:"", \
            self._TAG_CA:"", \
            self._TAG_CERT:"", \
            self._TAG_KEY:"", \
            self._TAG_DH:"", \
            self._TAG_SERVER:"", \
            self._TAG_IPPOOL:"", \
            self._TAG_C2C:"", \
            self._TAG_KALIVE:"", \
            self._TAG_TLS:"", \
            self._TAG_MAXC:"", \
            self._TAG_STAUS:"", \
            self._TAG_LOG:""}

    def _var_clear(self):
        for key in self._val_dic:
            self._val_dic[key] = ""

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
                    self._val_dic[key] = line.strip('\n')

        return self._val_dic
    
    def conf_flush(self):
        """
        Write modified options into the config file
        """
        conf_file = open(self._path, 'r')
        context = conf_file.read()
        conf_file.close()

        for key in self._val_dic:
            if not self._val_dic[key] == "":
                context = re.sub(self._re_dic[key], self._val_dic[key], context, 1, re.M)

        conf_file = open(self._path, 'w')
        conf_file.write(context)
        conf_file.close()

    def set_port(self, port):
        """
        Set the port number in the file
        """
        self.set_port_var(port)

        self.vpn_line_update_re(self._re_dic[self._TAG_PORT], port)

    def set_port_var(self, port):
        """
        Set the port variable
        """
        self._val_dic[self._TAG_PORT] = port

    def get_port(self):
        """
        Get the port number
        """
        return self._val_dic[self._TAG_PORT]

    def set_proto(self, proto):
        """
        Set the protocal type in the file
        """
        self.set_proto_var(proto)

        self.vpn_line_update_re(self._re_dic[self._TAG_PROTO], proto)

    def set_proto_var(self, proto):
        """
        Set the protocal variable
        """
        self._val_dic[self._TAG_PROTO] = proto

    def get_proto(self):
        """
        Get the protocal type
        """
        return self._val_dic[self._TAG_PROTO]
    
    def set_dev(self, dev):
        """
        Set the device in the file
        """
        self.set_dev_var(dev)

        self.vpn_line_update_re(self._re_dic[self._TAG_DEV], dev)

    def set_dev_var(self, dev):
        """
        Set the device variable
        """
        self._val_dic[self._TAG_DEV] = dev

    def get_dev(self):
        """
        Get the device 
        """
        return self._val_dic[self._TAG_DEV]

    def set_ca(self, ca):
        """
        Set the ca certificate in the file
        """
        self.set_ca_var(ca)

        self.vpn_line_update_re(self._re_dic[self._TAG_CA], ca)

    def set_ca_var(self, ca):
        """
        Set the ca certificate variable
        """
        self._val_dic[self._TAG_CA] = ca

    def get_ca(self):
        """
        Get the ca certificate 
        """
        return self._val_dic[self._TAG_CA]

    def set_cert(self, cert):
        """
        Set the server certificertte in the file
        """
        self.set_cert_var(cert)

        self.vpn_line_update_re(self._re_dic[self._TAG_CERT], cert)

    def set_cert_var(self, cert):
        """
        Set the server certificertte variable
        """
        self._val_dic[self._TAG_CERT] = cert

    def get_cert(self):
        """
        Get the server certificertte 
        """
        return self._val_dic[self._TAG_CERT]

    def set_key(self, key):
        """
        Set the server key in the file
        """
        self.set_key_var(key)

        self.vpn_line_update_re(self._re_dic[self._TAG_KEY], key)

    def set_key_var(self, key):
        """
        Set the server key variable
        """
        self._val_dic[self._TAG_KEY] = key

    def get_key(self):
        """
        Get the server key 
        """
        return self._val_dic[self._TAG_KEY]

    def set_dh(self, dh):
        """
        Set the server dh in the file
        """
        self.set_dh_var(dh)

        self.vpn_line_update_re(self._re_dic[self._TAG_DH], dh)

    def set_dh_var(self, dh):
        """
        Set the server dh variable
        """
        self._val_dic[self._TAG_DH] = dh

    def get_dh(self):
        """
        Get the server dh 
        """
        return self._val_dic[self._TAG_DH]

    def set_server(self, server):
        """
        Set the vpn ip range in the file
        """
        self.set_server_var(server)

        self.vpn_line_update_re(self._re_dic[self._TAG_SERVER], server)

    def set_server_var(self, server):
        """
        Set the vpn ip range variable
        """
        self._val_dic[self._TAG_SERVER] = server

    def get_server(self):
        """
        Get the vpn ip range
        """
        return self._val_dic[self._TAG_SERVER]

    def set_ippool(self, ippool):
        """
        Set the ifconfig-pool-persist in the file
        """
        self.set_ippool_var(ippool)

        self.vpn_line_update_re(self._re_dic[self._TAG_IPPOOL], ippool)

    def set_ippool_var(self, ippool):
        """
        Set the ifconfig-pool-persist variable
        """
        self._val_dic[self._TAG_IPPOOL] = ippool

    def get_ippool(self):
        """
        Get the ifconfig-pool-persist
        """
        return self._val_dic[self._TAG_IPPOOL]

    def set_c2c(self, c2c):
        """
        Set the client-to-client in the file
        """
        self.set_c2c_var(c2c)

        self.vpn_line_update_re(self._re_dic[self._TAG_C2C], c2c)

    def set_c2c_var(self, c2c):
        """
        Set the client-to-client variable
        """
        self._val_dic[self._TAG_C2C] = c2c

    def get_c2c(self):
        """
        Get the client-to-client
        """
        return self._val_dic[self._TAG_C2C]

    def set_kalive(self, kalive):
        """
        Set the keepalive in the file
        """
        self.set_kalive_var(kalive)

        self.vpn_line_update_re(self._re_dic[self._TAG_KALIVE], kalive)

    def set_kalive_var(self, kalive):
        """
        Set the keepalive variable
        """
        self._val_dic[self._TAG_KALIVE] = kalive

    def get_kalive(self):
        """
        Get the keepalive
        """
        return self._val_dic[self._TAG_KALIVE]

    def set_tls(self, tls):
        """
        Set the tls-auth in the file
        """
        self.set_tls_var(tls)

        self.vpn_line_update_re(self._re_dic[self._TAG_TLS], tls)

    def set_tls_var(self, tls):
        """
        Set the tls-auth variable
        """
        self._val_dic[self._TAG_TLS] = tls

    def get_tls(self):
        """
        Get the tls-auth
        """
        return self._val_dic[self._TAG_TLS]
    
    def set_maxc(self, maxc):
        """
        Set the max-clients in the file
        """
        self.set_maxc_var(maxc)

        self.vpn_line_update_re(self._re_dic[self._TAG_MAXC], maxc)

    def set_maxc_var(self, maxc):
        """
        Set the max-clients variable
        """
        self._val_dic[self._TAG_MAXC] = maxc

    def get_maxc(self):
        """
        Get the max-clients
        """
        return self._val_dic[self._TAG_MAXC]

    def set_status(self, status):
        """
        Set the status log in the file
        """
        self.set_status_var(status)

        self.vpn_line_update_re(self._re_dic[self._TAG_STATUS], status)

    def set_status_var(self, status):
        """
        Set the status log variable
        """
        self._val_dic[self._TAG_STATUS] = status

    def get_status(self):
        """
        Get the status log
        """
        return self._val_dic[self._TAG_STATUS]

    def set_log(self, log):
        """
        Set the log in the file
        """
        self.set_log_var(log)

        self.vpn_line_update_re(self._re_dic[self._TAG_LOG], log)

    def set_log_var(self, log):
        """
        Set the log variable
        """
        self._val_dic[self._TAG_LOG] = log

    def get_log(self):
        """
        Get the log
        """
        return self._val_dic[self._TAG_LOG]


if __name__ == "__main__":
    
    vpn_conf = VpnConf("./Resource/server2.conf");
    print vpn_conf.get_conf_options()
    vpn_conf.set_port("port 1776")
    vpn_conf.set_c2c("#client-to-client")
    vpn_conf.conf_flush()
    print vpn_conf.is_exist()



