#!/usr/bin/env python
#
# Fetch event (earthquake) information from the catalogs submitted to the IRIS DMC.
#
# Author: Mijian Xu, Tao Gou @ Nanjing University
#
# History: 2016-05-03, Init code, Mijian Xu
#          2016-05-07, Create opt function, Tao Gou
#          2016-06-02, Modify date and time options, Mijian Xu
#          2017-01-09, Fix bugs in Usage, Mijian Xu
#

import sys
import getopt
from sft.util import Events, get_time
try:
    import urllib.request as rq
except:
    import urllib as rq

def Usage():
    print("Usage: get_events.py -b<start-time> -e<end-time> [-R<minlon>/<maxlon>/<minlat>/<maxlon>]\n"
          "\t[-D<centerlat>/<centerlon>/<minradius>/<maxradius>] [-H<mindepth>/<maxdepth>]\n"
          "\t [-M<minmag>/<maxmag>[/<magtype>]] [-c<Catalog>] [-O[+c][+s<time>|<mag>]]")
    print("    -D RADIAL search terms (incompatible with the box search)")
    print("    -H Limit to events with depth between this range.")
    print("    -M Limit to events with magnitude between this range.\n"
          "       minmag: Limit to events with a magnitude larger than or equal to the specified minimum.\n"
          "       maxmag: Limit to events with a magnitude smaller than or equal to the specified maximum.\n"
          "       magtype: Specify magnitude type e.g., ML, Ms, mb, Mw\n")
    print("    -O Output parameters\n"
          "       -O[+c][+s<time>|<mag>]\n"
          "         +c If -c specified results should not include station and channel comments.\n"
          "         +s Order results by \"time\" or \"magnitude\", (\"time\" is default).")
    print("    -R BOX search terms (incompatible with radial search)")
    print("    -b Limit to events occurring on or after the specified start time.\n"
          "       Date and time format: YYYY-MM-DDThh:mm:ss (e.g., 1997-01-31T12:04:32)\n"
          "                             YYYY-MM-DD (e.g., 1997-01-31)")
    print("    -c Specify the catalog from which origins and magnitudes will be retrieved.\n"
          "       avaliable catalogs: ANF, GCMT, ISC, UoFW, NEIC")
    print("    -e Limit to events occurring on or before the specified end time\n"
          "       with the same date and time format as \"-b\".")

def opt():
    lalo_label = ''
    dep_label = ''
    mag_label = ''
    sort_label = ''
    cata_label = ''
    iscomment = True
    isreverse = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "R:D:b:e:c:H:M:O:")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)
    if sys.argv[1:] == []:
        print("No argument is found")
        Usage()
        sys.exit(1)
    if not ("-b" in [op for op, value in opts] and "-e" in [op for op, value in opts]):
        print("\"-b\" and \"-e\" must be specified.")
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
        elif op == "-b":
            begintime = get_time(value)
        elif op == "-e":
            endtime = get_time(value)
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
        elif op == "-O":
            for sub_op in value.split("+")[1:]:
                if sub_op[0] == "s":
                    if value.lower() == 'mag':
                        sort_label = 'orderby=magnitude' + '&'
                    elif value.lower() == 'time':
                        sort_label = ''
                    else:
                        print("Wrong option of \"-s\"")
                        sys.exit(1)
                elif sub_op[0] == "c":
                    iscomment = False
                elif sub_op[0] == "r":
                    isreverse = True
                else:
                    print("Invalid arguments in \"-O\"")
                    sys.exit(1)
        else:
            print("Invalid arguments")
            Usage()
            sys.exit(1)
    date_label = "start="+begintime.strftime("%Y-%m-%dT%H:%M:%S")+\
                 "&end="+endtime.strftime("%Y-%m-%dT%H:%M:%S")+"&"
    return lalo_label, dep_label, mag_label, cata_label, date_label, sort_label, iscomment, isreverse

def main():
    lalo_label, dep_label, mag_label, cata_label, date_label, sort_label, iscomment, isreverse = opt()
    events = Events(lalo_label, dep_label, mag_label, cata_label, date_label, sort_label, iscomment, isreverse)
    events.download()
    events.output()

if __name__ == '__main__':
    main()
