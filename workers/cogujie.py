#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lisnb
# @Date:   2015-10-12 22:56:47
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-13 00:04:20

import sys
sys.path.append('..')
import config

from book import Book 
from mogu import Mogu 
from mtcheckdup import MTCheckDup
import logging
import time



class Cogujie(object):
    """docstring for Cogujie"""
    def __init__(self, categories):
        super(Cogujie, self).__init__()
        self.categories = categories if type(categories) is list else [categories] 

    def run(self):
        logging.debug('Cogujie in, start running...')
        # if type(self.categories) is not list:
            # categories = [categories]
        # print categories
        for category in self.categories:
            # print category
            self.processcategory(category)

        if config.switch['mt']:
            while 1:
                time.sleep(1)


    # @classmethod
    def processcategory(self, category):
        print category
        logging.debug('process category: %(category)s, %(title)s, %(id)s'%category)
        book = Book(category['category'], bookid = category['id'], title = category['title'])
        mtcheckdup = MTCheckDup()
        
        if config.switch['mt']:
            for i in range(config.count['mogu']):
                t = Mogu(book, mtcheckdup)
                t.setDaemon(True)
                t.start()
        else:
            t = Mogu(book, mtcheckdup)
            t.run()

if __name__ == '__main__':
    categories = {
        'category': 'neiyi',
        'id': 50040,
        'title': u'内衣'
    }

    cogujie = Cogujie(categories)
    cogujie.run()



        