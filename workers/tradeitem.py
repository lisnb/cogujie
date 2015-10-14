#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 19:05:39
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-14 23:58:04

import sys
sys.path.append('..')
import config
import requests
import json
import os
import logging
import random
import time
from toolkit.util import Util

class TradeItem(object):
    """docstring for TradeItem"""

    def __init__(self, itemid, title = None, categorytitle = None, category = None, singleitemlimit = config.limit['singleitem']):
        super(TradeItem, self).__init__()
        self.itemid = itemid
        self.title = title if title else u'未知商品'
        self.category = category if category else 'not_specified'
        self.categorytitle = categorytitle if categorytitle else u'未知品类'
        self.singleitemlimit = singleitemlimit
        # self.title  = title
        # self.category = category
        # self.categorytitle = categorytitle

    def __str__(self):
        content = '%s\n%s\n%s\n\n%s'%(self.categorytitle, self.itemid, self.title, '\n'.join(self.parameter))
        return content.encode('utf-8')

    def run(self):
        logging.info('start tradeitem, itemid: %s, title: %s'%(self.itemid, self.title))
        self.__prepare()
        self.__getdetail()
        self.__getimgs()
        self.__writetofile()

    def __prepare(self):
        self.db = os.path.join(config.path['db'], self.category, self.itemid)
        # if not os.path.isdir(self.db):
            # os.makedirs(self.db)
        self.db_img = os.path.join(self.db, 'imgs')
        if not os.path.isdir(self.db_img):
            os.makedirs(self.db_img)

    def __getimgs(self):
        cnt = 0
        for img in self.imgs:
            imgdest = os.path.join(self.db_img, img['name'])
            Util.downloadimg(img['url'], imgdest, img['name'])
            cnt+=1
            if cnt >= self.singleitemlimit:
                break

    def __writetofile(self):
        dest = os.path.join(self.db, 'info')
        try:
            with open(dest, 'wb') as f:
                f.write(str(self))
        except Exception, e:
            logging.exception('%s writetofile exception'%self.itemid)

    def __getdetail(self):
        url = config.url['detail']%self.itemid
        detail = Util.http_get(url)
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

        self.parameter.append('\n')

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


if __name__ == '__main__':
    # Cogujie._downloadimg('sdaf')
    # logging.basicConfig(level = config.loglevel, format='%(asctime)s - %(levelname)s - %(threadName)-10s - %(message)s')
    logging.getLogger("requests").setLevel(logging.ERROR)
    cogujie  = TradeItem('18033m4')
    cogujie.run()



