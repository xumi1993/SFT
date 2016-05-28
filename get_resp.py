#!/usr/bin/env python
#
# Fetch instrumental response file (sacpz or resp) based on IRIS-WS
#
# Author: Mijian Xu
# 
# History: 2016-05-28 Init codes, Mijian Xu
#
import re
import sys
import getopt
from datetime import datetime
from util import Response

def Usage():
    print('get_resp')

def opt():
    location = "*"
    channel = "*"
    istime = 0
    timeinfo = []
    ispz = False
    outpath = './'
    try:
        opts,args = getopt.getopt(sys.argv[1:], "n:s:l:c:Y:O:P")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)
    if sys.argv[1:] == []:
        print("No argument is found")
        Usage()
        sys.exit(1)
    
    for op, value in opts:
        if op == "-n":
            network = value
        elif op == "-s":
            station = value
        elif op == "-l":
            location = value
        elif op == "-c":
            channel = value
        elif op == "-Y":
            yrange_sp = value.split('/')
            if len(yrange_sp) == 3:
                istime = 1
                timeinfo = [datetime.strptime(value, "%Y/%m/%d")]
            elif len(yrange_sp) == 6:
                istime = 2
                timeinfo = [datetime.strptime("%s/%s/%s" % tuple(yrange_sp[0:3]), "%Y/%m/%d"),
                        datetime.strptime("%s/%s/%s" % tuple(yrange_sp[3:6]), "%Y/%m/%d")]
            else:
                print("Invalid date format")
                sys.exit(1)
        elif op == "-P":
            ispz = True
        elif op == "-O":
            outpath = value
        else:
            print("Invalid arguments")
            sys.exit(1)


    return network, station, location, channel, istime, timeinfo, ispz, outpath

def main():
    network, station, location, channel, istime, timeinfo, ispz, outpath = opt()
    resp = Response(network, station, location, channel, istime, timeinfo, ispz)
    resp.download(outpath)

if __name__ == '__main__':
    main()
