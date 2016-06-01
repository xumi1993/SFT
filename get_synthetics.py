#!/usr/bin/env python
"""
Download synthetics data by 'URL Builder: syngine v.1'
"""

import sys
import getopt
from util import Syngines

def opt():
    source     = ''
    receiver   = ''
    data_range = ''
    model      = ''
    format_out = ''
    misc_ops   = ''
    try:
        opts,args = getopt.getopt(sys.argv[1:],"S:R:D:M:F:O:")
    except:
        print("Invalid Argument.  001")
#        Usage()
        sys.exit(1)

    for op,value in opts:
        if op == '-S':
            s_log = value[0].lower()
            if s_log == 'e':
                source = 'eventid='+value[1:]+'&'
            elif ('m','d','f').count(s_log):
                origin_t = value[1:].split(',')[0]
                s_loc    = value[1:].split(',')[1]
                s_lat    = s_loc.split('/')[0]
                s_lon    = s_loc.split('/')[1]
                s_dep    = s_loc.split('/')[2]
                mech      = value[1:].split(',')[2:]
                origintime = 'origintime='+origin_t+'&'
                source_loc = 'sourcelatitude='+s_lat+'&sourcelongitude='+s_lon+'&sourcedepthinmeters='+s_dep+'&'
                if s_log == 'm' and len(mech) == 6:
                    source_m = 'sourcemomenttensor='+mech[0]+','+mech[1]+','+mech[2]+','+mech[3]+','+mech[4]+','+mech[5]+'&'
                elif s_log == 'd' and len(mech) == 4:
                    source_m = 'sourcedoublecouple='+mech[0]+','+mech[1]+','+mech[2]+','+mech[3]+'&'
                elif s_log == 'd' and len(mech) == 3:
                    source_m = 'sourcedoublecouple='+mech[0]+','+mech[1]+','+mech[2]+'&'
                elif s_log == 'f' and len(mech) == 3:
                    source_m = 'sourceforce='+mech[0]+','+mech[1]+','+mech[2]+'&'
                else:
                    print("Error in SOURCE OPTIONS!")
                    sys.exit(1)
                source = origintime + source_loc + source_m
        elif op == '-R':
            r_log = value[0].lower()
            if r_log == 'c':
                r_lat = value[1:].split('/')[0]
                r_lon = value[1:].split('/')[1]
                receiver = 'receiverlatitude='+r_lat+'&receiverlongitude='+r_lon+'&'
            elif r_log == 's':
                stacoda  = value[1:]
                receiver = 'stationcoda='+stacoda+'&'
            elif r_log == 'n':
                if len(value[1:].split('.')) == 1:
                    network  = value[1:]
                    receiver = 'network='+network+'&'
                elif len(value[1:].split('.')) == 2:
                    network  = value[1:].split('.')[0]
                    station  = value[1:].split('.')[1]
                    receiver = 'network='+network+'&station='+station+'&'
                else:
                    print("Error in RECEIVER OPTIONS!")
                    sys.exit(1)
            else:
                print("Error in RECEIVER OPTIONS!")
                sys.exit(1)
        elif op == '-D':
            se = value.split('/')
            if len(se) == 1:
                endtime = se[0].replace('+','%2B')
                data_range = 'endtime='+endtime+'&'
            elif len(se) == 2:
                starttime = se[0].replace('+','%2B')
                endtime = se[1].replace('+','%2B')
                data_range = 'starttime='+starttime+'&endtime='+endtime+'&'
            else:
                print("Error in DATA RANGE OPTIONS!")
                sys.exit(1)
        elif op == '-M':
            mod = value.lower()
            if ('iasp91_2s','ak135f_5s','prem_a_5s','prem_a_10s','prem_a_20s').count(mod):
                model = 'model='+mod+'&'
            else:
                print("No model: "+mod)
                sys.exit(1)
        elif op == '-F':
            format_o = value.lower()
            if ('sac','saczip').count(format_o):
                format_out = 'format=saczip&'
            elif ('mini','miniseed','seed').count(format_o):
                format_out = 'format=miniseed&'
            else:
                print("There are two formats: saczip & miniSEED")
                sys.exit(1)
        elif op == '-O':
            label = ''
            components = ''
            units = 'units=velocity&'
            dt = ''
            kernel_width = ''
            amplitude_scale = ''
            for ss in value.split(','):
                if ss[0].lower() == 'l':
                    label = 'label='+ss[1:]+'&'
                elif ss[0].lower() == 'c':
                    components = 'components='+ss[1:]+'&'
                elif ss[0].lower() == 'u':
                    unit_value = ss[1:].lower()
                    if ('d','dis','displacement').count(unit_value):
                        units = 'units=displacement&'
                    elif ('v','vel','velocity').count(unit_value):
                        units = 'units=velocity&'
                    elif ('a','acceleration').count(unit_value):
                        units = 'units=acceleration&'
                    else:
                        print("No Units: "+unit_value+'.The units are set to be velocity.')
                        units = 'units=velocity&'
                elif ss[0].lower() == 's':
                    sample_interval = ss[1:].lower()
                    dt = 'dt='+sample_interval+'&'
                elif ss[0].lower() == 'k':
                    kernel_width = 'kernelwidth='+ss[1:]+'&'
                elif ss[0].lower() == 'a':
                    amplitude_scale = 'scale='+ss[1:]+'&'
            misc_ops = label+components+units+dt+kernel_width+amplitude_scale
    return source,receiver,data_range,model,format_out,misc_ops

def main():
    source,receiver,data_range,model,format_out,misc_ops = opt()
    synthetics = Syngines(source,receiver,data_range,model,format_out,misc_ops)
#    synthetics = Syngines('Source Options','Receiver Options','Data Range Options','Model','Format','Misc Options').download()
    synthetics.download()

if __name__ == '__main__':
    main()

# get_synthetics.py -Sd2010-02-07T02:23:46,23.6/47/63000,1e22,1e22,1e22 -RnIU.ANMO -D1000 -Miasp91_2s -Fsaczip -Oltest,cZ,s0.2
