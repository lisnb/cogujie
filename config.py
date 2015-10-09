#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 19:02:15
# @Last Modified by:   LiSnB
# @Last Modified time: 2015-10-09 20:12:54

import os
import logging

loglevel = logging.DEBUG

logging.basicConfig(level = loglevel, format='%(asctime)s - %(levelname)s - %(threadName)-10s - %(message)s')

root = 'E:\\tutorial\\python\\cogujie\\'

path = {
    'db': os.path.join(root, 'mogujie.db'),
}

url = {
    'detail': 'http://shop.mogujie.com/detailinfo/%s?_ajax=1',
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}

sleep = {
    'short': [1, 5],
    'long': [5, 10],
    'long long': [10, 15],
}