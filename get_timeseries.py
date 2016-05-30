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
from util import Timeseries

def Usage():
    print("get_timeseries")

def opt():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:s:l:c:S:")
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

    return network, station


def main():
    network, station = opt()
#    print(Timeseries('IU','ANMO','00','BHZ','2010-02-27T06:30:00','2010-02-27T10:30:00','miniseed')._format)
#     download = Timeseries('IU','ANMO','00','BHZ','2010-02-27T06:30:00','2010-02-27T10:30:00','miniseed').download()
#    download = Timeseries('IU','ANMO','00','BHZ','2010-02-27T06:30:00','2010-02-27T10:40:00','miniseed').download()
    print(station)
if __name__ == '__main__':
    main()
