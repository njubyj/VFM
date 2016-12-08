#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author = 'yjbao'

import unittest
import sys
sys.path.append(".")
from Deploy.vpn_xml import VpnXml
import Deploy.vpn_global_var as G
from Test import test_vars as T

class TestXML(unittest.TestCase):
    """
    'VpnXML' test class
    """   

    def setUp(self):
        pass
    #def test_get_guide_path(self):
    #    """
    #    Test: VpnXML.get_guide_path
    #    """
    #    g_path = self.__xml.get_guide_path()
    #    self.assertEqual(g_path, T.xml_guide_path)

    #def test_get_vpn_dir(self):
    #    v_dir = self.__xml.get_vpn_dir()
    #    self.assertEqual(v_dir, T.xml_vpn_dir)

    def test_get_user_cnt(self):
        self.__xml = VpnXml(T.xml_common_path)
        self.assertEqual(T.xml_usr_cnt, self.__xml.get_user_cnt())

    def test_get_server_cnt(self):
        self.__xml = VpnXml(T.xml_common_path)
        self.assertEqual(T.xml_sev_cnt, self.__xml.get_server_cnt())

    def test_is_usr_exist(self):
        self.__xml = VpnXml(T.xml_common_path)
        t = self.__xml.is_usr_exist(T.xml_usr_list[0])
        f = self.__xml.is_usr_exist("test_asdf")
        self.assertTrue(t)
        self.assertFalse(f)

    def test_add_del(self):
        self.__xml = VpnXml(T.xml_ad_path)
        self.__xml.xml_add_usr(T.xml_usr_list[0], "1", T.xmlt_usr_dir)
        tcnt = self.__xml.get_user_cnt()
        self.assertEqual(tcnt, T.xmla_ust_cnt)
        self.assertTrue(self.__xml.is_usr_exist(T.xml_usr_list[0]))
        
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
