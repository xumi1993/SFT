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
    network = ''
    station = ''
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

    ops = [op for op, value in opts]
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
    if "-b" in ops and "-e" in ops:
        timeinfo = [begintime, endtime]
    elif "-t" in ops:
        timeinfo = [pointtime]
    elif not ("-b" in ops or "-e" in ops or "-t" in ops):
        timeinfo = []
    elif ("-b" in ops or "-e" in ops and "-t" in ops):
        print("The given time is incompatible with start-time or end-time")
        sys.exit(1)
    else:
        print("Error option of datetime limitation")
        sys.exit(1)
    return network, station, location, channel, timeinfo, ispz, outpath

def main():
    network, station, location, channel, timeinfo, ispz, outpath = opt()
    resp = Response(network, station, location, channel, timeinfo, ispz)
    resp.download(outpath)

if __name__ == '__main__':
    main()
