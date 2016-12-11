#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "yjbao"

import os
import platform
import re

class VpnFile(object):
    """
    File Operation
    """

    # self._path: string 

    _file_sys = platform.system()

    def __init__(self, path):
        self._path = path

    def __get_line_idxW(self, text):
        """ 
        Get the line number with windows dos
        @file: target file 
        @text: content
        @return: line number or -1 
        """
        
        cmd = r'findstr /n "' + text + '" ' + self._path

        res = os.popen(cmd)
        line = res.read().strip().split(':', 1)[0]
        res.close()

        if not line:
            return -1

        return int(line)

    def __get_line_idxL(self, text):
        """ 
        Get the line number with linux shell
        @file: target file 
        @text: content
        @return: line number or -1 
        """

        cmd = 'grep -n "' + text + '" ' + self._path + ' '
        cmd += " | awk -F ':' '{print$1}'"

        res = os.popen(cmd)
        line = res.read().strip()
        res.close()

        if not line:
            return -1

        return int(line)

    def __vpn_file_line_updateL(self, old, new):
        """ 
        Replace the line with new context 
        @file: target file
        @old: old content
        @new: new content
        """

        line = self.__get_line_idxL(old)

        if not line:
            return False

        cmd = 'sed -i "' + str(line) + 's/.*/' + new + '/" ' + self._path

        res = os.popen(cmd)
        code = res.read().strip()
        res.close()

        if code == "":
            return True

        return False

    def __vpn_get_fileL(self, path, key):
        """ 
        Get the file name in the path according to the key
        @path: directory
        @key: key word 
        @return: the name of file
        """

        cmd = "ls " + path
        cmd += ' | grep "' + key + '"'

        res = os.popen(cmd)
        name = res.read().strip()
        res.close()

        return name

    def get_path(self):
        """
        Get the path of the file
        """
        return self._path

    def get_file(self):
        """
        Get the file name 
        """
        return os.path.basename(self._path)

    def is_exist(self):
        """
        Detect the file whether is valid or not
        """
        return os.path.isfile(self._path)

    def get_file_line_idx(self, text):
        """ 
        Get the line number in the file
        @file: target file 
        @text: content
        @return: line number or -1 
        """
        #if not os.path.isfile(self._path):
        #    return False

        if self._file_sys == "Windows":
            return self.__get_line_idxW(text)
        else:
            return self.__get_line_idxL(text)

    def vpn_line_update_re(self, old, new, count = 1):
        """ 
        Replace the old with new string in the file
        @path: target file
        @old: old string regular
        @new: new string 
        """
        #if not os.path.isfile(self._path):
        #    return False

        tar_file = open(self._path, 'r')
        tar_old = tar_file.read()
        tar_file.close()
                  
        tar_new = re.sub(old, new, tar_old, count, flags = re.M)
        #if tar_new == tar_old:
        #    return False
        tar_file = open(self._path, 'w')
        tar_file.write(tar_new)
        tar_file.close()
