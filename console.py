#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 20:15:10
# @Last Modified by:   LiSnB
# @Last Modified time: 2015-10-10 14:24:38

from workers import cogujie
import sys



def run(itemid):
    instance = cogujie.Cogujie(itemid)
    # instance.run()


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        print 'need an item id'
        exit(1)
    itemid = args[1]
    run(itemid)



