#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-10 20:38:12
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-10 23:15:42

import sys
sys.path.append('..')
import config

import re
from toolkit.util import Util
from Queue import Queue
import threading
import logging
import time

class Book(object):
    """docstring for Book"""
    def __init__(self, category, bookid, title = u'未知品类', sectionlimit = config.limit['section']):
        super(Book, self).__init__()
        self.category = category
        self.bookid = bookid
        self.title = title
        self.currentpage = 1
        self.page = 0
        self.currentsection = 1
        self.section = 0
        self.itemqlock = threading.Lock()
        self.items = Queue()
        self.book = ''
        self.over = False
        self.batchlimit = batchlimit

    def __iter__(self):
        return self

    def __getfirstsection(self):
        logging.debug('get portal... ')
        url = config.path['book']%(self.category, self.page)
        html = Util.http_get(url)
        if not html:
            logging.error('no portal html, category: {}, bookid: {}'.format(self.category, self.bookid))
            exit(2)
        profile = config.regex['profile'].search(html)
        if not profile or 'profile' not in profile.groupdict():
            logging.error('no profile, category: {}, bookid: {}'.format(self.category, self.bookid))
            exit(3)
        else:
            profile = json.loads(profile.groupdict()['profile'])
        self.book = profile.get('book', '')
        if not self.book:
            logging.error('no valid book, category: {}, bookid: {}'.format(self.category, self.bookid))
            exit(4)
        firstdata = config.regex['firstdata'].search(html)
        if not firstdata or 'firstdata' not in firstdata.groupdict():
            logging.error('no firstdata, category: {}, bookid: {}'.format(self.category, self.bookid))
            exit(5)
        else:
            firstdata = json.loads(firstdata.groupdict()['firstdata'])
        for item in firstdata:
            self.items.put(item)

    def __getnextsection(self):
        if self.section >= self.batchlimit


    def next(self):
        with self.itemqlock:
            if self.over:
                raise StopIteration
            if self.items.qsize() == 0:
                r = self.__getnextsection()
                if not r:
                    logging.info('book done, category: {}, bookid: {}'.format(self.category, self.bookid))
                    self.over = True
                    raise StopIteration
            item = self.items.get()
        return item



class MTIter(object):
    def __init__(self):
        self.tid = 0
        self.tlock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        with self.tlock:
            tid = self.tid
            self.tid += 1
            if self.tid > 20:
                raise StopIteration
        return tid

class MTIWorker(threading.Thread):
    """docstring for MTIWorker"""
    def __init__(self, mtiter):
        super(MTIWorker, self).__init__()
        self.mtiter = mtiter

    def run(self):
        for i in self.mtiter:
            print '{}, {}'.format(self.name, i)
            time.sleep(1)

def testmti():
    mtiter = MTIter()
    for i in range(5):
        t = MTIWorker(mtiter)
        # t.setDaemon(True)
        t.start()

    # while 1:
        # time.sleep(1)

if __name__ == '__main__':
    testmti()


