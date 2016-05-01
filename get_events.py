#!/usr/bin/env python

import re
import sys
import getopt
try:
    import urllib.request as rq
except:
    import urllib as rq

def Usage():
    print("Usage: get_events.py -Yminyear/minmonth/minday/maxyear/maxmonth/maxday [-Rminlon/maxlon/minlat/maxlon] [-Dcenterlat/centerlon/minradius/maxradius] [-Hmindepth/maxdepth] [-Mminmag/maxmag[/magtype]] [-cCatalog] [-stime|mag]")
    print("-Y -- Limit to events occurring between this range.")
    print("-R -- BOX search terms (incompatible with radial search)")
    print("-D -- RADIAL search terms (incompatible with the box search)")
    print("-H -- Limit to events with depth between this range.")
    print("-M -- Limit to events with magnitude between this range.\n\
            Specify magnitude type e.g., ML, Ms, mb, Mw")
    print("-c -- Specify the catalog from which origins and magnitudes will be retrieved.\n\
            avaliable catalogs: ANF, GCMT, ISC, UoFW, NEIC")
    print("-s -- Order results by time or magnitude, default in time.")

lalo_label = ''
dep_label = ''
date_label = ''
mag_label = ''
sort_label = ''
cata_label = ''
try:
    opts,args = getopt.getopt(sys.argv[1:], "R:D:Y:c:H:M:s:")
except:
    print("Invalid arguments")
    Usage()
    sys.exit(1)
if sys.argv[1:] == []:
    print("No argument is found")
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
        if len(mon1) == 1:
            mon1 = '0'+mon1
        if len(day1) == 1:
            day1 = '0'+day1
        if len(mon2) == 1:
            mon2 = '0'+mon2
        if len(day2) == 1:
            day2 = '0'+day2
        date_label = 'start='+year1+'-'+mon1+'-'+day1+'T00:00:00&end='+year2+'-'+mon2+'-'+day2+'T00:00:00&'
    elif op == "-c":
        cata_label = 'catalog='+value+'&'
    elif op == "-M":
        mag1 = value.split("/")[0]
        mag2 = value.split("/")[1]
        if len(value.split("/")) == 2:
            mag_label = 'minmag='+mag1+'&maxmag='+mag2+'&'
        else:
            mtype = value.split("/")[2]
            mag_label = 'minmag='+mag1+'&maxmag='+mag2+'&magtype='+mtype+'&'
    elif op == "-S":
        if value.lower() == 'mag':
            sort_label = 'orderby=magnitude&'
        else:
            sort_label = ''
    else:
        print("Invalid arguments")
        Usage()
        sys.exit(1)

url = 'http://service.iris.edu/fdsnws/event/1/query?format=text&'
url += lalo_label+dep_label+mag_label+cata_label+date_label
url = url[:-1]
try:
    response = rq.urlopen(url)
except:
    print("No data is found")
    sys.exit(1)
evt_lst = response.readlines()
for evt in evt_lst:
    evt = evt.decode().strip()
    if evt[0] == '#':
        continue
    print(evt)
