#!/usr/bin/env python
#
# Fetch instrumental response file (sacpz or resp) based on IRIS-WS
#
# Author: Mijian Xu @ Nanjing University
# 
# History: 2016-05-28 Init codes, Mijian Xu
#          2016-06-01 Fix options of datetime, Mijian Xu
#          2016-06-14 Add usage, Mijian Xu

import re
import sys
import getopt
from util import Response, get_time

def Usage():
    print("Usage: get_resp -n<Network> -s<Station> [-l<Location>] [-c<Channel>]\n"
          "      [-b<start-time>] [-e<end-time>] [-t<Timestamp>] [-o<Outpath>] [-P]")

def opt():
    location = "*"
    channel = "*"
    timeinfo = []
    ispz = False
    outpath = './'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:s:l:c:b:e:t:o:P")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)
    if not sys.argv[1:]:
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
        elif op == "-b":
            begintime = get_time(value)
        elif op == "-e":
            endtime = get_time(value)
        elif op == "-t":
            pointtime = get_time(value)
        elif op == "-P":
            ispz = True
        elif op == "-o":
            outpath = value
        else:
            print("Invalid arguments")
            sys.exit(1)
    if "-b" in op and "-e" in op:
        timeinfo = [begintime, endtime]
    elif "-t" in op:
        timeinfo = [pointtime]
    elif not ("-b" in op or "-e" in op or "-t" in op):
        timeinfo = []
    else:
        print("Wrong option of datetime limitation")
    return network, station, location, channel, timeinfo, ispz, outpath

def main():
    network, station, location, channel, timeinfo, ispz, outpath = opt()
    resp = Response(network, station, location, channel, timeinfo, ispz)
    resp.download(outpath)

if __name__ == '__main__':
    main()
