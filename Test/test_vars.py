#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author = 'yjbao'


### tag variables
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



app_dir = "/usr/apps/OpenVPN"




### xml test variables
xml_test_path = "./Test/TestXML/"
xml_common_path = xml_test_path + "vpnxml.xml"
# get/detect
xml_usr_cnt = 1
xml_sev_cnt = 1
xml_sev_idx = 2
xml_usr_list = ["test_tenant"]
xml_sev_list = ["server1"]
# add/delete 
xml_ad_path = xml_test_path + "add_del.xml"
xmlt_usr_dir = app_dir + "/z_test_tenant"
xmla_ust_cnt = 1
xmld_ust_cnt = 0
xmla_sev_cnt = 1
xmld_sev_cnt = 0
xmlau_sev_idx = 2
xmlau_sev_cnt = 1
xmldu_sev_idx = 2
xmldu_sev_cnt = 0
xml_conf_dic = {\
        TAG_PORT:"1779", \
        TAG_PROTO:"udp", \
        TAG_DEV:"tap3", \
        TAG_CA:"/usr/apps/OpenVPN/z_test_tenant/config/ca.crt", \
        TAG_CERT:"/usr/apps/OpenVPN/z_test_tenant/config/server1.crt", \
        TAG_KEY:"/usr/apps/OpenVPN/z_test_tenant/config/server1.key", \
        TAG_DH:"/usr/apps/OpenVPN/z_test_tenant/config/dh1024.pem", \
        TAG_SERVER:"10.9.3.0 255.255.255.0", \
        TAG_IPPOOL:";", \
        TAG_C2C:"1", \
        TAG_KALIVE:"10 120", \
        TAG_TLS:"/usr/apps/OpenVPN/z_test_tenant/config/ta.key", \
        TAG_MAXC:";", \
        TAG_STATUS:"/usr/apps/OpenVPN/z_test_tenant/log/server1_status.log", \
        TAG_LOG:"/usr/apps/OpenVPN/z_test_tenant/log/server1_log.log"}




### guide test variables
guide_test_path = ".\\Test\\TestGuide\\"
guide_none_path = guide_test_path + "guide_none.conf"
guide_normal_path = guide_test_path + "guide_normal.conf"

