#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 19:15:17
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-10 23:31:31
import sys
sys.path.append('../..')

import config
import requests
import json
import logging
import random
import time


class Util(object):
    """docstring for Util"""
    def __init__(self, arg):
        super(Util, self).__init__()
        self.arg = arg

    @classmethod
    def downloadimg(cls, src, dest, name):
        logging.debug('img - downloading: %s'%src)
        cls.sleep('short')
        try:
            r = requests.get(src)
            with open(dest, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024):
                    f.write(chunk)
        except Exception, e:
            logging.exception('img - downloading exception: %s'%name)

    @classmethod
    def http_get(cls, url, headers = config.header):
        try:
            response = requests.get(url, headers = headers)
            return response.content
        except Exception, e:
            logging.exception('get url: %s'%url)
            return None

    @classmethod
    def http_post(cls, url, payload, headers = config.header):
        try:
            response = requests.post(url, data = payload, headers = headers)
            return response.content
        except Exception, e:
            logging.exception('post url: %s'%url)
            return None


    @classmethod
    def sleep(cls, interval):
        sec = config.sleep[interval]
        sec = random.randint(sec[0], sec[1])
        time.sleep(sec)
