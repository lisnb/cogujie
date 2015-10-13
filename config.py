#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 19:02:15
# @Last Modified by:   LiSnB
# @Last Modified time: 2015-10-13 16:30:08

import os
import logging
import re
import platform

system = platform.system().lower()

# root = os.getcwd()
root = os.path.split(os.path.realpath(__file__))[0]

level = {
    'log': logging.INFO,
}

path = {
    'db': os.path.join(root, 'mogujie.db'),
}

count = {
    'mogu': 5,
}

switch = {
    'mogucheckdup': True,
    'mt': False
}

limit = {
    'section': 20,
    'singlepage': 9,
    'mogudup': 10,
    'singleitem': 5,
}

url = {
    'detail': 'http://shop.mogujie.com/detailinfo/%s?_ajax=1',
    'portalbook': 'http://www.mogujie.com/book/%s/%s',
    'ajaxbook': 'http://www.mogujie.com/book/ajax',
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}

sleep = {
    'short': [1, 5],
    'long': [5, 10],
    'long long': [10, 15],
}

regex = {
    'profile': re.compile(r'MOGUPROFILE = [\w\W]+?book:"(?P<book>[^"]+?)"'),
    'firstdata': re.compile(r'MoGu.APP.firstData = ((?P<firstdata>\[[\w\W]+?\]);)'),
}


logging.basicConfig(level = level['log'], format='%(asctime)s - %(levelname)s - %(threadName)-10s - %(message)s')