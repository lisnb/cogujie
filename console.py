#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 20:15:10
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-12 20:22:43

from workers import cogujie
import sys
import logging



def clearfix():
    pass

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



