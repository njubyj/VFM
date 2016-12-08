#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author = 'yjbao'

import unittest
import ConfigParser as CP
import sys
sys.path.append(".")
from Deploy.vpn_guide import VpnGuideParser
from Test import test_vars as T

class TestXML(unittest.TestCase):
    """
    'VpnXML' test class
    """   

    def setUp(self):
        self._conf = CP.ConfigParser()

    def test_get_client_none(self):
        clt_list = VpnGuideParser(T.guide_none_path).get_clients()
        self.assertEqual(clt_list, []);

    def test_get_servers(self):
        sev_list = VpnGuideParser(T.guide_none_path).get_servers()
        self.assertEqual(sev_list, []);

    def test_get_client_normal(self):
        clt_list = VpnGuideParser(T.guide_normal_path).get_clients()
        self.assertEqual(len(clt_list), 2)
        tmp_list = [\
            ("test1", {"name":"anylink_1200012", "task":"add"}), \
            ("test2", {"name":"anylink_1200013", "task":"del"})]
        self.assertEqual(cmp(clt_list, tmp_list), 0)

    def test_get_server_normal(self):
        sev_list = VpnGuideParser(T.guide_normal_path).get_servers()
        self.assertEqual(len(sev_list), 4)
        tmp_list = [\
            ("test1", \
             {"name":"server1", "port":"1194", "proto":"UDP", "dev":"tap", \
              "server":"10.8.0.0", "client-to-client":"1", "keepalive":"10 120", \
              "task":"add"}), \
            ("test2", {"name":"server2", "task":"del"}), \
            ("test3", \
             {"name":"server3", "port":"1194", "proto":"UDP", "dev":"tap", \
              "server":"10.8.0.0", "client-to-client":"1", "keepalive":"10 120", \
              "task":"up"}), \
            ("test4", {"name":"server4", "task":"sea"})]
        self.assertEqual(cmp(sev_list, tmp_list), 0)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity = 2)
    #f = open("test.txt", "w+")
    #runner = unittest.TextTestRunner(f, verbosity = 2)
    #runner.run(unittest.makeSuite(TestXML, "test"))
    