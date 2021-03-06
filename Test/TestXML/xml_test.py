﻿#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author = 'yjbao'

import unittest
import shutil
import sys
sys.path.append(".")
from Deploy.vpn_xml import VpnXml
import Deploy.vpn_global_var as G
from Test import test_vars as T
#import xml.etree.ElementTree as ET

class TestXML(unittest.TestCase):
    """
    'VpnXML' test class
    """   

    def setUp(self):
        pass

    def test_get(self):
        self.__xml = VpnXml(T.xml_common_path)
        self.assertEqual(T.xml_usr_cnt, self.__xml.get_user_cnt())
        self.assertEqual(T.xml_sev_cnt, self.__xml.get_server_cnt())
        self.assertEqual(T.xml_sev_idx, self.__xml.get_usr_sevidx(T.xml_usr_list[0]))

    def test_is_usr_exist(self):
        self.__xml = VpnXml(T.xml_common_path)
        t = self.__xml.is_usr_exist(T.xml_usr_list[0])
        f = self.__xml.is_usr_exist("test_asdf")
        self.assertTrue(t)
        self.assertFalse(f)
        t = self.__xml.is_server_exist(T.xml_usr_list[0], T.xml_sev_list[0])
        f = self.__xml.is_server_exist(T.xml_usr_list[0], "server_sss")
        self.assertTrue(t)
        self.assertFalse(f)

    def test_add_del(self):
        shutil.copyfile(T.xml_bak_path, T.xml_ad_path)
        self.__xml = VpnXml(T.xml_ad_path)
        self.__xml.xml_add_usr(T.xml_usr_list[0], "1", T.xmlt_usr_dir)
        tcnt = self.__xml.get_user_cnt()
        self.assertEqual(tcnt, T.xmla_ust_cnt)
        self.assertTrue(self.__xml.is_usr_exist(T.xml_usr_list[0]))

        self.__xml.xml_add_server(T.xml_usr_list[0], T.xml_sev_list[0], \
            T.xml_conf_dic)
        scnt = self.__xml.get_server_cnt()
        uscnt = self.__xml.get_usr_sevcnt(T.xml_usr_list[0])
        sidx = self.__xml.get_usr_sevidx(T.xml_usr_list[0])
        self.assertEqual(scnt, T.xmla_sev_cnt)
        self.assertEqual(uscnt, T.xmlau_sev_cnt)
        self.assertEqual(sidx, T.xmlau_sev_idx)
        self.assertTrue(self.__xml.is_server_exist(T.xml_usr_list[0], T.xml_sev_list[0]))

        self.__xml.xml_del_server(T.xml_usr_list[0], T.xml_sev_list[0])
        scnt = self.__xml.get_server_cnt()
        uscnt = self.__xml.get_usr_sevcnt(T.xml_usr_list[0])
        sidx = self.__xml.get_usr_sevidx(T.xml_usr_list[0])
        self.assertEqual(scnt, T.xmld_sev_cnt)
        self.assertEqual(uscnt, T.xmldu_sev_cnt)
        self.assertEqual(sidx, T.xmldu_sev_idx)
        self.assertFalse(self.__xml.is_server_exist(T.xml_usr_list[0], T.xml_sev_list[0]))
        
        self.__xml.xml_del_usr(T.xml_usr_list[0])
        tcnt = self.__xml.get_user_cnt()
        self.assertEqual(tcnt, T.xmld_ust_cnt)
        self.assertFalse(self.__xml.is_usr_exist(T.xml_usr_list[0]))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity = 2)
    #f = open("test.txt", "w+")
    #runner = unittest.TextTestRunner(f, verbosity = 2)
    #runner.run(unittest.makeSuite(TestXML, "test"))
