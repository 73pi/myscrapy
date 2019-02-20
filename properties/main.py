# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         main
# Description:  
# Author:       73
# Date:         2019/2/19
#-------------------------------------------------------------------------------

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "manual"])
# debug运行main
