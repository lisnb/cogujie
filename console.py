#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2015-10-09 20:15:10
# @Last Modified by:   lisnb
# @Last Modified time: 2015-10-14 23:42:26

from workers.cogujie import Cogujie
from workers.tradeitem import TradeItem
import sys
import logging
import getopt
import config
import json
import os



def clearfix():
    logging.getLogger('requests').setLevel(logging.WARNING)
    # pass

def usage():
    usage = """

    # @Author: LiSnB
    # @Date:   2015-10-09 20:15:10
    # @Last Modified by:   lisnb
    # @Last Modified time: 2015-10-13 16:48:43
    # @E-mail: lisnb.h@hotmail.com

    NAME
            cogujie - Mogujie images crawler
    SYNOPSIS
            python cogujie.py -h
            python cogujie.py -i --iid= [--it=] [--cid=] [--cat=] [--ct=]
            python cogujie.py -c --cat= --cid= [--ct=] [--tc=]
            python cogujie.py -c -s --csf= [--mt] [--tc=]
    DESCRIPTION
            cogujie is used to crawl the images from http://mogujie.com.
            You can configure it in config.py.
            You can crawl a single trade item or all the trade items under a category.
            All the images will be stored in mogujie.db, structure is orgnized as below:

            mogujie.db
            ├── skirt_50099
            │   └── 180ohb6
            │       ├── imgs
            │       │   ├── 180ohb6_model_img_0.jpg
            │       │   ├── 180ohb6_model_img_1.jpg
            │       │   ├── 180ohb6_model_img_2.jpg
            │       │   ├── 180ohb6_model_img_3.jpg
            │       │   └── 180ohb6_model_img_4.jpg
            │       └── info
            └── t.placeholder
            
            The content of info file is as below ('ln' means nth line):
            l1: the title of the category to which this item belongs
            l2: the tradeitemid of current item
            l3: the title of current item
            l4 - : some parameter of this item

            multi-thread is enabled, the number of threads can be set in the config file.
    OPTIONS
            -h  --help
                help information, print this usage
            -i
                single item mode, --iid must be provided
            --iid
                in single item mode, iid imply the specific item that need to be processed
                so it's necessary
            --it
                the title of the specific item
                it not provideda default value will be used
            -c
                category mode, all items under this category will be processed
                (a limit can be set in config file)
            --cat
                necessary in category mode, optional in single item mode.
                the category name, eg: clothing, neiyi etc.
            --cid
                necessary in category mode, optional in single item mode.
                the sub identification of the category, usually a number
            --ct
                optional in both mode, the title of the category
            -s
                instead of process a single category, by using this option,
                you can provide a bunch of categories in a file using --csf option
            --csf
                the file full of categories, necessary when you specify the -s option.
                the file is supposed to be in JSON format.
                3 fields must be specified like the sample file.
            --mt
                if mt is specified, each category in the given file
                will be processed at same time using multi-threads
                or they will be processed one by one.
            --tc
                how many threads will be used to process a category
    """
    print usage

def run():
    clearfix()
    opt = 'icshv'
    lopt = ['csf=','iid=', 'it=', 'cid=', 'cat=', 'ct=', 'tc=', 'mt', 'help']
    opts, args = getopt.getopt(sys.argv[1:], opt, lopt)
    optd= dict(opts)

    iid = optd.get('--iid', None)
    it = optd.get('--it', None)
    csf = optd.get('--csf', None)
    cid = optd.get('--cid', None)
    cat = optd.get('--cat', None)
    ct = optd.get('--ct', None)

    if '--tc' in optd and optd['--tc']>0:
        config.count['mogu'] = tc
    if '--mt' in optd:
        config.switch['mt'] = True

    help_ = '--help' in optd or '-h' in optd

    if '-' in optd:
        logging.basicConfig(level = logging.DEBUG, format='%(asctime)s - %(levelname)s - %(threadName)-10s - %(message)s')

    if help_:
        usage()
        exit(0)

    elif '-i' in optd and '-c' not in optd:
        """given item"""
        if not iid:
            print 'the itemid is necessary, use iid option to specify one'
            print ' or use --help or -h to check the usage'
            exit(1)
        category = '%s_%s'%(cat, cid) if cat and cid else None
	it = it if not it else it.decode('utf-8')
        tradeitem = TradeItem(iid, it, ct, category)
        tradeitem.run()

    elif '-c' in optd and '-i' not in optd:
        """given category"""
        if '-s' not in optd:
            #single category
            if not cid or not cat:
                print 'the category and category id are necessary, use cat and cid to specify'
                print ' or use --help or -h to check the usage'
                exit(1)
            category = {
                'category': cat,
                'id': cid,
                'title': ct if not ct else ct.decode('utf-8')
            }
            cogujie = Cogujie(category)
            cogujie.run()
        else:
            #json file
            print csf
            if not csf or not os.path.isfile(csf):
                print 'a valid category file is necessary, use csf to specify'
                print ' or use --help or -h to check the usage'
                exit(1)
            with open(csf, 'rb') as f:
                c = f.read()
            categories = json.loads(c)
            cogujie = Cogujie(categories)
            cogujie.run()

    elif '-c' not in optd and '-i' not in optd:
        print 'you are supposed to provided one of  -i -c at'
        print 'use --help or -h to check the usage'
        exit(1)

    else:
        print 'you are not supposed to provided -i -c at the same time'
        print 'use --help or -h to check the usage'
        exit(1)




if __name__ == '__main__':
    run()
    exit(0)
    args = sys.argv
    if len(args) == 1:
        print 'need an item id'
        exit(1)
    itemid = args[1]
    run(itemid)



