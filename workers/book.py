#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-10 20:38:12
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-11 00:07:40

import sys
sys.path.append('..')
import config

import re
from toolkit.util import Util
from Queue import Queue
import threading
import logging
import time
import json
import base64

class Book(object):
    """docstring for Book"""
    def __init__(self, category, bookid, title = u'未知品类', sectionlimit = config.limit['section'], singlepagelimit = config.limit['singlepage']):
        super(Book, self).__init__()
        self.category = category
        self.bookid = bookid
        self.title = title
        self.currentpage = 1
        # self.page = 0
        self.currentsection = 2
        self.section = 1
        self.itemqlock = threading.Lock()
        self.items = Queue()
        self.book = ''
        self.over = False
        self.sectionlimit = sectionlimit
        self.singlepagelimit = singlepagelimit
        self.payload = {
            'section': 1,
            'location': 'clothing',
            'book': '',
        }
        self.__getfirstsection()

    def __iter__(self):
        return self

    def __getfirstsection(self):
        logging.debug('get portal... ')
        url = config.url['portalbook']%(self.category, self.currentpage)
        html = Util.http_get(url)
        if not html:
            logging.error('no portal html, category: {}, bookid: {}, page: {}'.format(self.category, self.bookid, self.currentpage))
            exit(2)
        profile = config.regex['profile'].search(html)
        if not profile or 'book' not in profile.groupdict():
            logging.error('no book, category: {}, bookid: {}, page: {}'.format(self.category, self.bookid, self.currentpage))
            exit(3)
        else:
            # print profile.groupdict()['book']
            self.book = profile.groupdict()['book']
            #profile = json.loads(profile.groupdict()['profile'])
        # self.book = profile.get('book', '')
        # exit(5)
        self.payload['book'] = self.book
        if not self.book:
            logging.error('no valid book, category: {}, bookid: {}, page: {}'.format(self.category, self.bookid, self.currentpage))
            exit(4)
        firstdata = config.regex['firstdata'].search(html)
        if not firstdata or 'firstdata' not in firstdata.groupdict():
            logging.error('no firstdata, category: {}, bookid: {}, page: {}'.format(self.category, self.bookid, self.currentpage))
            exit(5)
        else:
            print firstdata.groupdict()['firstdata']
            firstdata = json.loads(firstdata.groupdict()['firstdata'])

        for item in firstdata:
            self.items.put(item)



    def __getnextsection(self):
        if self.section >= self.sectionlimit:
            return False
        if self.currentpage == self.singlepagelimit:
            self.currentpage+=1
            self.section+=1
            self.currentsection = 2
            self.__getfirstsection()
            return self.items.qsize()>0

        self.payload['section'] = self.currentsection
        response = Util.http_post(config.url['ajaxbook'], self.payload)
        if not response:
            logging.warning('getnextsection response null, payload: %s'%self.payload)
            return False
        try:
            items = json.loads(response)
            if 'result' not in items or 'list' not in items['result'] or not items['result']['list']:
                logging.warning('getnextsection list null, payload: %s'%self.payload)
                return False
            else:
                items = items['result']['list']
                for item in items:
                    self.items.put(item)
                return self.items.qsize>0
        except Exception, ex:
            logging.exception('getnextsection exception: %s'%self.payload)
            return False


    def next(self):
        with self.itemqlock:
            if self.over:
                raise StopIteration
            if self.items.qsize() == 0:
                r = self.__getnextsection()
                if not r:
                    logging.info('book done, category: {}, bookid: {}, page: {}'.format(self.category, self.bookid, self.currentpage))
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
    book = Book('neiyi', 50030)
    for item in book:
        print item['tradeItemId'], item['title']


