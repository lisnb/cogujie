#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2015-10-10 22:52:43
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-10 23:11:39

"""
import sys
sys.path.append('../..')

import config
"""

import threading


class MTCheckDup(object):
    """docstring for MTCheckDup"""
    def __init__(self, func = None):
        super(MTCheckDup, self).__init__()
        self.__slock = threading.Lock()
        self.__items = set()
        # if not func:
        #     def returnself(item):
        #         return item
        #     self.func = returnself
        # else:
        #     self.func = func

    def checkdup(self, item, func = None):
        if not item:
            return True
        key = func(item) if func else item
        if not key:
            return True
        with self.__slock:
            inset = key in self.__items
        return inset

    def inserttoset(self, item, func = None):
        if not item:
            return
        key = func(item) if func else item
        if not key:
            return True
        with self.__slock:
            self.__items.add(key)

    def checkandinsert(self, item, func = None):
        if not item:
            return True
        key = func(item) if func else item
        with self.__slock:
            inset  = key in self.__items
            if not inset:
                self.__items.add(key)
        return inset


if __name__ == '__main__':
    def func(item):
        return item[:2]
    mt = MTCheckDup()
    print mt.checkdup('abd', func)
    print mt.checkdup('abc', func)
    mt.inserttoset('abd', func)
    print mt.checkdup('abc', func)
    print mt.checkandinsert('bac')
    print mt.checkdup('bac')
    # print mt.__items
    print dir(mt)


