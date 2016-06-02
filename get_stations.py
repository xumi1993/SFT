#!/usr/bin/env python
#
# Fetch stations in IRIS DMC based on IRIS-WS
#
# Author: Mijian Xu, Tao Gou @ Nanjing University
#
# History: 2016-05-03, Init code, Mijian Xu
#          2016-05-07, Create opt function, Tao Gou
#          2016-05-30, Modify date and time options, Mijian Xu
#          2016-06-02, Add options of -C -G -S -A, Mijian Xu
#

import sys
import getopt
from util import Stations, get_time
try:
    import urllib.request as rq
except:
    import urllib as rq

def Usage():
    print("Usage: get_events.py [-b start-time] [-e end-time]"
          "[-Rminlon/maxlon/minlat/maxlon]\n\t [-Dcenterlat/centerlon/minradius/maxradius] "
          "[-nNetwork] [-sStation]\n\t [-lLocation] [-cChannel] [-Llevel] [-C] [-G] [-S] [-A]")
    print("-A -- Specify if results should include information about time series data availability at the channel level. (False default)")
    print("-C -- If -C specified results should not include station and channel comments.")
    print("-D -- RADIAL search terms (incompatible with the box search)")
    print("-G -- Create a script to plot these stations on a global map (require GMT-5.x.x).")
    print("-L -- Specify level of detail using 'network', 'station', 'channel' or 'response'")
    print("-R -- BOX search terms (incompatible with radial search)")
    print("-S -- Do not display whether results should include information relating to restricted channels. (True default)")
    print("-b -- Limit to events occurring on or after the specified start time.\n"
            "\tDate and time format: YYYY-MM-DDThh:mm:ss (e.g., 1997-01-31T12:04:32)\n"
            "\t                      YYYY-MM-DD (e.g., 1997-01-31)")
    print("-c -- Specify channel code")
    print("-e -- Limit to events occurring on or before the specified end time \n"\
          "\twith the same date and time format as \"-b\".")
    print("-l -- Spicify locations code (Use \"--\" for \"Blank\" location).")
    print("-n -- Specify network code")
    print("-s -- Specify station code")

def opt():
    lalo_label = ''
    net_label = ''
    sta_label = ''
    loc_label = ''
    cha_label = ''
    dateb_label = ''
    datee_label = ''
    level_label = ''
    restri_label = ''
    avalib_label = ''
    isgmt = False
    iscomment = True
    try:
        opts, args = getopt.getopt(sys.argv[1:], "R:D:b:e:c:n:s:l:L:CSAG")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)

    allop = [op for op, value in opts]
    if allop.count("-R") and allop.count("-D"):
        print("CONNOT specify -R and -D at the same time")
        Usage()
        sys.exit(1)
    elif allop == []:
        Usage()
        sys.exit(1)

    for op, value in opts:
        if op == "-R":
            lon1 = value.split("/")[0]
            lon2 = value.split("/")[1]
            lat1 = value.split("/")[2]
            lat2 = value.split("/")[3]
            lalo_label = 'minlat='+lat1+'&maxlat='+lat2+'&minlon='+lon1+'&maxlon='+lon2+'&'
        elif op == "-D":
            lat = value.split("/")[0]
            lon = value.split("/")[1]
            dist1 = value.split("/")[2]
            dist2 = value.split("/")[3]
            lalo_label ='lat='+lat+'&lon='+lon+'&maxradius='+dist2+'&minradius='+dist1+'&'
        elif op == "-n":
            net_label = 'net='+value+'&'
        elif op == "-s":
            sta_label = 'sta='+value+'&' 
        elif op == "-l":
            loc_label = 'loc='+value+'&'
        elif op == "-c":
            cha_label = 'cha='+value+'&'
        elif op == "-b":
            begintime = get_time(value)
            dateb_label = 'start='+begintime.strftime("%Y-%m-%dT%H:%M:%S")+'&'
        elif op == "-e":
            endtime = get_time(value)
            datee_label = 'end='+endtime.strftime("%Y-%m-%dT%H:%M:%S")+'&'
        elif op == "-L":
            level = value.lower()
            level_label = 'level='+level+'&'
        elif op == "-C":
            iscomment = False
        elif op == "-S":
            restri_label = "includerestricted=false&"
        elif op == "-A":
            avalib_label = "includeavailability=true&"
        elif op == "-G":
            isgmt = True
        else:
            print("Invalid arguments")
            sys.exit(1)

    return lalo_label, net_label, sta_label, loc_label, cha_label,\
            dateb_label, datee_label, level_label, iscomment, isgmt, \
            restri_label, avalib_label

def main():
    lalo_label, net_label, sta_label, loc_label, cha_label,\
            dateb_label, datee_label, level_label, \
            iscomment, isgmt, restri_label, avalib_label = opt()
    stations = Stations(lalo_label, net_label, sta_label, loc_label, cha_label,\
            dateb_label, datee_label, level_label, iscomment, restri_label, avalib_label)
    stations.download()
    stations.output()
    if isgmt:
        stations.gmt_script()

if __name__ == '__main__':
   main()

