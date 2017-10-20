#!/usr/bin/env python
# Fetch travel time based on IRIS-WS
# 
# Author: Mijian Xu, Haibo Wang
#
# History: 2016-05-27 Init Code, Haibo Wang
#          2016-06-06 Add output option, Mijian Xu
#

"""
Get Traveltime data by 'URL Builder: traveltimes v.1'
"""
import sys
import getopt
from sft.util import Traveltime

def Usage():
    print('Usage: get_traveltime.py -Mmodel -Pphase1[/phase2[/phase3...]] -Hevent_depth -D<d,k,e>distance [-O[+c][+m][+aT|R]]')
    print('    -M Specify the Model, three models( iasp91, prem, ak135) are available.')
    print('    -P Specify the phase you need. Comma or solidus separate list of phases. See Taup Doucmentation for more information.')
    print('    -H Specify the depth of the event, in kilometers.')
    print('    -D Specify the distance.')
    print('         -Dd<value>: distance in degrees. For example, -Dd30 means distance=30 degrees.')
    print('         -Dk<value>: distance in kilometers. For example, -Dk3000 means distance=3000 kilometers.')
    print('         -De<evlat/evlon/stlat/stlon>: distance in event location and station location.')
    print('    -O Output parameters.')
    print('        +c Suppresses header from the resulting table.')
    print('        +m only retrieve the first arrival of each phase for each distance.')
    print('        +a<T|R> returns a space–separated list of travel times in seconds (\"T\").\n'
          '              or return a space-separated list of ray parameters in sec/deg (\"R\").')
    print('    -h or --help  For help.')

def opt():
    model_label  = 'model=iasp91&'
    phases_label = ''
    evdp_label   = ''
    dist_label   = ''
    out_label = ''
    try:
        opts,args = getopt.getopt(sys.argv[1:],"M:P:H:D:O:h",["help"])
    except:
        print("\n    Invalid Arguments.\n")
        Usage()
        sys.exit(1)
    if sys.argv[1:] == []:
        print("No argument is found")
        Usage()
        sys.exit(1)
    
    for op,value in opts:
        if op in ("-h",'--help'):
            Usage()
            sys.exit(1)
        if op == "-M":
            model = value.lower()
            if ('iasp91','prem','ak135').count(model):
                model_label = 'model='+model+'&'
            else:
                print("Model must be specify as iasp91, prem or ak135")
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
                print("Error in distance information.")
                Usage()
                sys.exit(1) 
        elif op == '-O':
            sub_argv = value[1:].split("+")
            for sub_op in sub_argv:
                if sub_op[0] == 'c':
                    out_label += 'noheader=true&'
                elif sub_op[0] == 'm':
                    out_label += 'mintimeonly=true&'
                elif sub_op[0] == 'a':
                    if len(sub_op) != 2:
                        print("Invalid arguments in \"-O+a\"")
                        sys.exit(1)
                    if sub_op[1] == 'T':
                        out_label += 'traveltimeonly=true&'
                    elif sub_op[1] == 'R':
                        out_label += 'rayparamonly=true&'
                    else:
                        print("Invalid arguments in \"-O+a\"")
                        sys.exit(1)
                else:
                    print("Invalid arguments in \"-O\"")
                    sys.exit(1)
        else:
            print("Invalid arguments")
            Usage()
            sys.exit(1)
    return model_label, phases_label, evdp_label, out_label, dist_label

def main():
    model_label, phases_label, evdp_label, out_label, dist_label = opt()
    travetimes = Traveltime(model_label, phases_label, evdp_label, out_label, dist_label)
    travetimes.download()
    travetimes.output()

if __name__ == '__main__':
    main()
