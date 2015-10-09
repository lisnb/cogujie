#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 19:05:39
# @Last Modified by:   LiSnB
# @Last Modified time: 2015-10-09 20:32:04

import sys
sys.path.append('..')
import config
import requests
import json
import os
import logging
import random
import time

class Cogujie(object):
    """docstring for Cogujie"""

    @staticmethod
    def _sleep(interval):
        sec = config.sleep[interval]
        sec = random.randint(sec[0], sec[1])
        time.sleep(sec)

    @staticmethod
    def _downloadimg(src, dest, name):
        logging.debug('img - downloading: %s'%src)
        Cogujie._sleep('short')
        try:
            r = requests.get(src)
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024):
                    f.write(chunk)
        except Exception, e:
            logging.exception('img - downloading exception: %s'%name)

    @staticmethod
    def _get(url):
        try:
            response = requests.get(url, headers = config.header)
            return response.content
        except Exception, e:
            logging.exception('get url: %s'%url)
            return None

    def __init__(self, itemid):
        super(Cogujie, self).__init__()
        self.itemid = itemid

    def run(self):
        self.getdetail()


    def prepare(self):
        self.db = os.path.join(config.path['db'], self.itemid)
        if not os.path.isdir(self.db):
            os.makedirs(self.db)
        self.db_img = os.path.join(self.db, 'imgs')
        if not os.path.isdir(self.db_img):
            os.mkdir(self.db_img)

    def getimgs(self):
        for img in self.imgs:
            imgdest = os.path.join(self.db_img, img['name'])
            Cogujie._downloadimg(img['url'], imgdest, img['name'])
    def __str__(self):
        content = '%s\n%s'%(self.itemid, '\n'.join(self.parameter))
        return content.encode('utf-8')

    def writetofile(self):
        dest = os.path.join(self.db, 'info')
        try:
            with open(dest, 'wb') as f:
                f.write(str(self))
        except Exception, e:
            logging.exception('%s writetofile exception'%self.itemid)

    def getdetail(self):
        self.prepare()
        url = config.url['detail']%self.itemid
        detail = Cogujie._get(url)
        try:
            detail = json.loads(detail)
            # logging.debug(detail)
            if not detail:
                logging.debug('%s no detail'%self.itemid)
                return
            if 'status' not in detail:
                logging.debug('%s no status'%self.itemid)
                return
            if 'code' not in detail['status']:
                logging.debug('%s no code'%self.itemid)
                return
            if detail['status']['code'] != 1001:
                logging.debug('%s code not 1001' % self.itemid)
                return
            if 'result' not in detail:
                logging.debug('%s no result'%self.itemid)
                return
            detail = detail['result']
        except Exception, e:
            logging.exception('%s exception'%self.itemid)
            return
        if 'parameter' not in detail or 'datas' not in detail['parameter']:
            logging.debug('%s no parameter'%self.itemid)
        else:
            self.parameter = detail['parameter']['datas']

        if 'modules' not in detail:
            logging.debug('%s no modules'%self.itemid)
        else:
            self.imgs = []
            imgid_ai = 0
            for module in detail['modules']:
                if 'images' not in module and module['images']:
                    continue
                self.parameter.append('%(key)s: %(name)s'%module)
                for img in module['images']:
                    curimg = {
                        'name': '%s_%s_%s.jpg'%(self.itemid, module.get('key', 'img'), imgid_ai),
                        'url': img['src']
                    }
                    self.imgs.append(curimg)
                    imgid_ai+=1

        self.getimgs()
        self.writetofile()

if __name__ == '__main__':
    # Cogujie._downloadimg('sdaf')
    # logging.basicConfig(level = config.loglevel, format='%(asctime)s - %(levelname)s - %(threadName)-10s - %(message)s')
    logging.getLogger("requests").setLevel(logging.ERROR)
    cogujie  = Cogujie('18033m4')
    cogujie.run()



