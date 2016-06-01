#!/usr/bin/env python
#
# Author: Mijian Xu, Tao Gou
#
# History: 2016-05-07 Init Code, Tao Gou
#          2016-05-30 Create API to command line, Mijian Xu
"""
Download timeseries data by 'URL Builder: timeseries v.1'
"""
import sys
import getopt
from datetime import datetime
from util import Timeseries, get_time

def Usage():
    print("get_timeseries -b start-time -e end-time -n network [-s station] [-l location]"
          "[-c channel] [-O outpath]")
    print("-b -- Specifies the desired start-time for data")
    print("-e -- Specify the end-time for the data")
    print("-n -- Select one or more network codes. Accepts wildcards and lists. "
          "Can be SEED codes or data center defined codes.")
    print("-s -- Select one or more SEED station codes. Accepts wildcards and lists.")
    print("-l -- Select one or more SEED location identifier. Accepts wildcards and lists. "
          "Use -- for \"Blank\" location IDs (ID’s containing 2 spaces).")
    print("-c -- Select one or more SEED channel codes. Accepts wildcards and lists.")
    print("-O -- Specify out path")
    print("See http://service.iris.edu/fdsnws/dataselect/1/ for more details.")

def opt():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:s:l:c:O:b:e:")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)
    if sys.argv[1:] == []:
        print("No argument is found")
        Usage()
        sys.exit(1)

    station = "*"
    location = "*"
    channel = "*"
    outpath = "./"
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
        elif op == "-O":
            outpath = value
        else:
            print("Invalid arguments")
            Usage()
            sys.exit(1)
    try:
        return network, station, location, channel, begintime, endtime, outpath
    except:
        print("The 'network', 'begintime', 'endtime' must be assumed")
        sys.exit(1)

def main():
    network, station, location, channel, begintime, endtime, outpath = opt()
    download = Timeseries(network, station, location, channel, begintime.strftime("%Y-%m-%dT%H:%M:%S"), endtime.strftime("%Y-%m-%dT%H:%M:%S"), 'miniseed').download(outpath)
if __name__ == '__main__':
    main()
