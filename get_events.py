#!/usr/bin/env python

import re
import sys
import getopt
try:
    import urllib.request as rq
except:
    import urllib as rq

lalo_label = ''
try:
    opts,args = getopt.getopt(sys.argv[1:], "R:D:Y:C:H:")
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
        
