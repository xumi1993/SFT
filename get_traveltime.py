#!/usr/bin/env python
# Fetch travel time based on IRIS-WS
# 
# Author: Mijian Xu, Haibo Wang
#
# History: 2016-05-27 Init Code, Haibo Wang
#

"""
Get Traveltime data by 'URL Builder: traveltimes v.1'
"""
import sys
import getopt
from util import Traveltime

def Usage():
    print('get_traveltime []')

def opt():
    model_label  = ''
    phases_label = ''
    evdp_label   = ''
    nohder_label = ''
    dist_label   = ''
    try:
        opts,args = getopt.getopt(sys.argv[1:], "M:P:H:D:C")
    except:
        print("Invalid Arguments 1")
        sys.exit(1)

    for op, value in opts:
        if op == "-M":
            model = value.lower()
            if ('iasp91','prem','ak135').count(model):
                model_label = 'model='+model+'&'
            else:
                print("Model should be:iasp91, prem or ak135")
                sys.exit(1)
        elif op == "-P":
            phases = value.replace('/',',')
            phases_label = 'phases='+phases+'&'
        elif op == "-H":
            evdep = value
            evdp_label = 'evdepth='+evdep+'&'
        elif op == "-D":
            distlog = value[0].lower()
            if distlog == 'd':
                degrees = value[1:]
                dist_label = 'distdeg='+degrees
            elif distlog == 'k':
                kilom = value[1:]
                dist_label = 'distkm='+kilom
            elif distlog == 'e':
                evlat = value[1:].split("/")[0]
                evlon = value[1:].split("/")[1]
                stlat = value[1:].split("/")[2]
                stlon = value[1:].split("/")[3]
                dist_label = 'evloc=['+evlat+','+evlon+']&staloc=['+stlat+','+stlon+']'
            else:
                print("Error: distance information...")
                sys.exit(1)
        elif op == '-C':
            nohder_label = 'noheader=true&'
        else:
            print("Invalid arguments")
            sys.exit(1)
    return model_label, phases_label, evdp_label, nohder_label, dist_label

def main():
    model_label, phases_label, evdp_label, nohder_label, dist_label = opt()
    travetimes = Traveltime(model_label, phases_label, evdp_label, nohder_label, dist_label)
    travetimes.download()
    travetimes.output()

if __name__ == '__main__':
    main()
