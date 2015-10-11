#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2015-10-11 14:39:48
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-11 14:58:20

import sys
sys.path.append('..')
import config

from book import book
from tradeitem import TradeItem
from toolkit.util import Util 
import threading


class Mogu(threading.Thread):
    """docstring for Mogu"""
    def __init__(self, book, checkdup):
        super(Mogu, self).__init__()
        self.book = book
        self.checkdup = checkdup
        self.checkdup.setfunc(self.__getkey)
        self.dupcnt = 0

    def __getkey(self, item):
        return item.get('tradeItemId', '')

    def run(self):
        logging.debug('mogu in start collecting ...')
        for item in self.book:
            try:
                if config.switch['mogucheckdup'] and self.checkdup.checkandinsert(item, self.__getkey):
                    self.dupcnt+=1
                    if self.dupcnt < config.limit['mogudup']:
                        logging.debug('item dup, current dupcnt: {}, current item: {}'.format(self.dupcnt, item))
                    else:
                        logging.warning('item dup badly, check your strategy and config')
                    continue
                titem = TradeItem(item['tradeItemId'], item.get('title', None))
                titem.run()
            except Exception, e:
                logging.exception('mogu exception, item: %s'%item)


def testdef():
    a = def t():
        return 0
    print a()

if __name__ == '__main__':
    testdef()
        