#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

import os

class VpnBase(object):
    """
    Manage VPN tenant server
    """

    def __init__(self):
        pass

    def vpn_shell(self, sh, param):
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

    def set_vpn(self, vpn):
        """
        Set VPN excute path
        @vpn: vpn path
        """
        pass

    def get_vpn(self):
        """
        Get VPN excute path
        """
        pass
    
    def vpn_create(self, rsa):
        """
        Create a directory by self
        @rsa: vpn shell path
        """
        pass

    def vpn_add_server(self, template, name, conf_dic):
        """
        Build a new server with 'conf_dic' config
        @template: server config template path
        @name: server config file name
        @conf_dic: server config options 
        """
        pass


    def vpn_start(self):
        """
        Start server 
        """
        pass

    def vpn_add_client(self, param, name):
        """
        Build a client 
        @param: parameters 
        @name: client name
        """
        pass
