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

    DEV_TAP = "tap"
    DEV_TUN = "tun"
    PROTO_UDP = "udp"
    PROTO_TCP = "tcp"
    SUF_CRT = ".crt"
    SUF_CSR = ".csr"
    SUF_KEY = ".key"
    SUF_PEM = ".pem"
    SUF_TXT = ".txt"
    SUF_LOG = ".log"
    SUF_PID = ".pid"
    CA_CRT = "ca.crt"
    CA_KEY = "ca.key"
    TA_KEY = "ta.key"
    DH_PEM1 = "dh1024.pem"
    DH_PEM2 = "dh2048.pem"
    IP_MASK8 = "255.255.255.0"
    IP_MASK16 = "255.255.0.0"
    IP_MASK24 = "255.0.0.0"
    SEV_NAME = "server"
    SIGN_IPP = "ipp"
    SIGN_LOG = "log"
    SIGN_STATUS = "status"
    VPN_CONF = ".conf"
    VPN_OVPN = ".ovpn"
    TIME_ALIVE = "10 120"

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
    XML_TAG_TEMPLATE = "template"
    XML_TAG_ = ""

    DIR_CONFIG = "config"
    DIR_KEYS = "keys"
    DIR_LOG = "log"

    VPN_OPS_DIC = {\
        TAG_PORT:"", \
        TAG_PROTO:"udp", \
        TAG_DEV:"", \
        TAG_CA:"", \
        TAG_CERT:"", \
        TAG_KEY:"", \
        TAG_DH:"", \
        TAG_SERVER:"", \
        TAG_IPPOOL:"", \
        TAG_C2C:"1", \
        TAG_KALIVE:"10 120", \
        TAG_TLS:"", \
        TAG_MAXC:";", \
        TAG_STATUS:"", \
        TAG_LOG:""}

    def __init__(self):
        pass