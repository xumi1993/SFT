#!/usr/bin/env python


import re
import sys
import getopt
from util import Stations
try:
    import urllib.request as rq
except:
    import urllib as rq

def opt():
   lalo_label = ''
   net_label = ''
   sta_label = ''
   loc_label = ''
   cha_label = ''
   date_label = ''
   try:
       opts,args = getopt.getopt(sys.argv[1:], "R:D:Y:c:n:s:l:")
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
       elif op == "-n":
           net_label = 'net='+value+'&'
       elif op == "-s":
           sta_label = 'sta='+value+'&'
       elif op == "-l":
           loc_label = 'loc='+value+'&'
       elif op == "-c":
           cha_label = 'cha='+value+'&'
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
           date_label = 'start='+year1+'-'+mon1+'-'+day1+'&end='+year2+'-'+mon2+'-'+day2+'&'
       else:
           print("Invalid arguments")
           sys.exit(1)

   return lalo_label, net_label, sta_label, loc_label, cha_label, date_label

def main():
   lalo_label, net_label, sta_label, loc_label, cha_label, date_label = opt()
   stations = Stations(lalo_label, net_label, sta_label, loc_label, cha_label, date_label)
   stations.download()
   stations.output()

if __name__ == '__main__':
   main()

