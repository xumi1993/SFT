#!/usr/bin/env python


import re
import sys
import getopt
try:
    import urllib.request as rq
except:
    import urllib as rq

lalo_label = ''
net_label = ''
sta_label = ''
loc_label = ''
cha_label = ''
date_label = ''
try:
    opts,args = getopt.getopt(sys.argv[1:], "R:D:Y:C:N:S:L:")
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
    elif op == "-N":
        net_label = 'net='+value+'&'
    elif op == "-S":
        sta_label = 'sta='+value+'&'
    elif op == "-L":
        loc_label = 'loc='+value+'&'
    elif op == "-C":
        cha_label = 'cha='+value+'&'
    elif op == "-Y":
        yrange_sp = value.split("/")
        year1 = yrange_sp[0]
        mon1 = yrange_sp[1]
        day1 = yrange_sp[2]
        year2 = yrange_sp[3]
        mon2 = yrange_sp[4]
        day2 = yrange_sp[5]
        date_label = 'start='+year1+'-'+mon1+'-'+day1+'&end='+year2+'-'+mon2+'-'+day2+'&'
    else:
        print("Invalid arguments")
        sys.exit(1)

url = "http://service.iris.edu/irisws/fedcatalog/1/query?"
url += lalo_label+net_label+sta_label+loc_label+cha_label+date_label
url = url[:-1]
response = rq.urlopen(url)
html = response.read().decode()
find_re = re.compile(r'\w+\s+\w+\s[^A-Za-z]{2}\s+\w+\s+\d+.+?\n',re.DOTALL)
sta_lst = find_re.findall(html)
if sta_lst == []:
    print("No data is found")
    sys.exit(1)
for sta_info in sta_lst:
    print(sta_info.strip())
