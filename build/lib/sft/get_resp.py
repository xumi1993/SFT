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
from sft.util import Response, get_time

def Usage():
    print("Usage: get_resp -n<Network> -s<Station> [-l<Location>] [-c<Channel>]\n"
          "      [-b<start-time>] [-e<end-time>] [-t<Timestamp>] [-o<Out-path>] [-P]")
    print("     -b Limit to events occurring on or after the specified start time.\n"
          "       -b<start-time>\n"
          "          Date and time format: YYYY-MM-DDThh:mm:ss (e.g., 1997-01-31T12:04:32)\n"
          "                                YYYY-MM-DD (e.g., 1997-01-31)")
    print("     -c Specify channel code. Accepts wildcards and lists.\n"
          "        -c<channel>")
    print("     -e Limit to events occurring on or before the specified end time \n"
          "        -e<end-time>\n"
          "           with the same date and time format as \"-b\".")
    print("     -l Spicify locations code (Use \"--\" for \"Blank\" location). Accepts wildcards and lists.\n"
          "        -l<location>")
    print("     -n Specify network code. Accepts wildcards and lists.\n"
          "        -n<network>")
    print("     -o Specify Out path\n"
          "        -o<Out-path>")
    print("     -P Specify the format of response files. If \"-P\" was specified will output sacpz file (default is RESP file)")
    print("     -s Specify station code. Accepts wildcards and lists.\n"
          "        -s<station>")
    print("     -t Find the response for the given time (incompatible with start-time or end-time)\n"
          "        -t<Timestamp>\n"
          "         The date format is same as -b option")
    print('   -h or --help For help.')


def opt():
    network = ''
    station = ''
    location = "*"
    channel = "*"
    timeinfo = []
    ispz = False
    outpath = './'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:s:l:c:b:e:t:o:Ph", ["help"])
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
        elif op in ("-h", "--help"):
            Usage()
            sys.exit(1)
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
