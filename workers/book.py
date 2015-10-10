#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-10 20:38:12
# @Last Modified by:   LiSnB
# @Last Modified time: 2015-10-10 20:41:22

import sys
sys.path.append('..')
import config

import re
from toolkit.util import Util


class Book(object):
    """docstring for Book"""
    def __init__(self, category, bookid, title = u'未知品类'):
        super(Book, self).__init__()
        self.category = category
        self.bookid = bookid
        self.title = title
        self.page = 1
        self.section = 1
    

