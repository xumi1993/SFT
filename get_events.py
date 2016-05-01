#!/usr/bin/env python

import re
import sys
import getopt
try:
    import urllib.request as rq
except:
    import urllib as rq

lalo_label = ''
dep_label = ''
date_label = ''
try:
    opts,args = getopt.getopt(sys.argv[1:], "R:D:Y:C:H:M:")
except:
    print("Invalid arguments")
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
    elif op == "-H":
        dep1 = value.strip("/")[0]
        dep2 = value.strip("/")[1]
        dep_label = 'mindepth='+dep1+'&maxdepth='+dep2+'&'
    elif op == "-Y":
        yrange_sp = value.split("/")
        year1 = yrange_sp[0]
        mon1 = yrange_sp[1]
        day1 = yrange_sp[2]
        year2 = yrange_sp[3]
        mon2 = yrange_sp[4]
        day2 = yrange_sp[5]
        date_label = 'start='+year1+'-'+mon1+'-'+day1+'&end='+year2+'-'+mon2+'-'+day2+'&'
    elif op == "-C":
        cata_label = value
    elif op == "-M":
        mag1 = value.split("/")[0]
        mag2 = value.split("/")[1]
        mtype = value.split("/")[2]
        mag_label = 'minmag='+mag1+'&maxmag='+mag2+'&magtype='+mtype+'&'
    else:
        print("Invalid arguments")
        sys.exit(1)

