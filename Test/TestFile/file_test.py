#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author = 'yjbao'

import unittest
import shutil
import os
import sys
sys.path.append(".")
from Deploy.vpn_file import VpnFile as VFILE
from Test import test_vars as T


class Test_file_test(unittest.TestCase):

    #get_file_line_idx
    #vpn_line_update_re
    #vpn_delete_line

    def setUp(self):
        #shutil.copyfile(T.file_bak_txt, T.file_del_txt)
        #shutil.copyfile(T.file_bak_txt, T.file_up_txt)
        pass

    def test_line_idx(self):
        file = VFILE(T.file_bak_txt)
        lineno = file.get_file_line_idx("CN=cc2")
        self.assertEqual(lineno, 3)

    def test_line_update_re(self):
        shutil.copyfile(T.file_bak_txt, T.file_up_txt)
        file = VFILE(T.file_up_txt)
        file.vpn_line_update_re(T.file_re_str, T.file_new_str)
        lineno = file.get_file_line_idx(T.file_new_str)
        self.assertEqual(lineno, 3)

    def test_delete_line(self):
        shutil.copyfile(T.file_bak_txt, T.file_del_txt)
        file = VFILE(T.file_del_txt)
        file.vpn_delete_line(T.file_key_str)
        lineno = file.get_file_line_idx(T.file_key_str)
        self.assertEqual(lineno, -1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity = 2)

    
