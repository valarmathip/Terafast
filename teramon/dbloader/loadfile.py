#!/usr/bin/python
import os, sys, time
import commands, re
import glob

from pysqllib import MySqlAccess


if __name__ == '__main__':

    mySqlHdlr = MySqlAccess('10.6.3.5','root','','flowmon')
    fileList = glob.glob("/home/ryu/csvfiles/flow*.Pending")
    for file in fileList:
        print "loading file %s \n" % (file)
        mySqlHdlr.load_file(file,'flow_table')
        os.system('\\rm "%s"' % file)

    fileList = glob.glob("/home/ryu/csvfiles/total*.Pending")
    for file in fileList:
        print "loading file %s \n" % (file)
        mySqlHdlr.load_file(file,'total_stats_table', ignoreHeader=False)
        os.system('\\rm "%s"' % file)
