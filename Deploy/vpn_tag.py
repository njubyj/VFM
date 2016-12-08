#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'yjbao'

class VpnTag(object):
    """
    Define some vpn tags
    """

    TAG_PORT = "port"
    TAG_PROTO = "proto"
    TAG_DEV = "dev"
    TAG_CA = "ca"
    TAG_CERT = "cert"
    TAG_KEY = "key"
    TAG_DH = "dh"
    TAG_SERVER = "server"
    TAG_IPPOOL = "ifconfig-pool-persist"
    TAG_C2C = "client-to-client"
    TAG_KALIVE = "keepalive"
    TAG_TLS = "tls-auth"
    TAG_MAXC = "max-clients"
    TAG_STATUS = "status"
    TAG_LOG = "log"

    SEC_VPN = "vpn"
    SEC_OPTIONS = "options"
    SEC_SERVER = "server"
    SEC_CLIENT = "client"
    OPT_KEYS = "keys"
    OPT_NAME = "name"
    OPT_USR = "usr"
    OPT_TASK = "task"
    TASK_ADD = "add"
    TASK_DEL = "del"
    TASK_UP = "up"
    TASK_SEA = "sea"

    XML_TAG_VFM = "vfm"
    XML_TAG_CLOUD = "cloud"
    XML_TAG_TAPIDX = "tapidx"
    XML_TAG_ADDRIDX = "addridx"
    XML_TAG_PORTIDX = "portidx"
    XML_TAG_USRIDX = "usridx"
    XML_TAG_VPNDIR = "vpn_dir"
    XML_TAG_RSA = "easy-rsa"
    XML_TAG_GUIDE = "guide"
    XML_TAG_LOGGER = "logger"
    XML_TAG_DATAXML = "dataxml"
    XML_TAG_ = ""
    XML_TAG_ = ""

    DIR_CONFIG = "config"
    DIR_KEYS = "keys"
    DIR_LOG = "log"

    VPN_CONF = ".conf"
    VPN_OVPN = ".ovpn"

    def __init__(self):
        pass