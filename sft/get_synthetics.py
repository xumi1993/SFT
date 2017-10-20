#!/usr/bin/env python
"""
Download synthetics data by 'URL Builder: syngine v.1'
"""

import sys
import getopt
from sft.util import Syngines

def Usage():
    print('Usage: get_synthetics.py -Ssourc_options -Rreceiver_options -Ddata_range_options [-Mmodel] [-F<format>] -Ooutpara')
    print('   -S  Source options.')
    print('     -Se<eventid> (Use eventID to define an event, The only catalog currently supported is Global CMT.)')
    print('     -Sm<origin_time,source_latitude/source_longitude/source_depth,moment_tensor>')
    print('     -Sd<origin_time,source_latitude/source_longitude/source_depth,double_couple>')
    print('     -Sf<origin_time,source_latitude/source_longitude/source_depth,force>')
    print('        The origin_time formats:')
    print('            YYYY-MM-DDThh:mm:ss[.ssssss]  ex. 1997-01-31T12:04:32.123')
    print('            YYYY-MM-DD                    ex. 1997-01-31 a time of 00:00:00 is assumed.')
    print('        The source depth is in meters.')
    print('        The mechanism components should be separated by comma and in particular orders')
    print('            For source_moment_tensor: Mrr,Mtt,Mpp,Mrt,Mrp,Mtp.')
    print('            For source_double_couple: strike,dip,rake[,M0].')
    print('            For source_force: Fr,Ft,Fp.')
    print('   -R  Receiver options.')
    print('     -Rc<receiver_latitude/receiver_longitude>')
    print('     -Rn<network[.station]>')
    print('     -Rs<stacode>')
    print('        Use network_code.station_code to identify receiver coordinates of a operating station.')
    print('        Use network_code to identify all the stations of the network.')
    print('   -D  Data range options.')
    print('     -D<start_time/endtime>')
    print('     -D<endtime>(The start time is assumed to be the origin time.)')
    print('        The time may be specified as either:')
    print('           An absolute date and time               ex. 1997-01-31T12:06:60')
    print('           A phase-relative offset                 ex. P-30')
    print('           An offset from origin time in seconds   ex. 30')
    print('        If the value is recognized as an absolute date and time, it is interpreted as an absolute time.')
    print('        If the value is in the form phase[+/-]offset, it is interpreted as a phase-relative time.')
    print('        If the value is a numerical value, it is interpreted as an offset, in seconds, from origin time')
    print('        for start time,and from start time for end time. And the end time should be positive.')
    print('   -M  Model.')
    print('     -M<model_name>')
    print('        List of models: iasp91_2s (default), ak135f_5s, prem_a_5s, prem_a_10s, prem_a_20s.')
    print('   -F  Format of output.')
    print('     -F<value>')
    print('        List of formats: \"saczip\" (ZIP archive of sac files, default), \"miniseed\".')
    print('   -O  Output parameters.')
    print('     -O[+l<label>][+c<components>][+u<units>][+s<sample_interval>][+k<kernel_width>][+a<amplitude_scale>]')
    print('       label: Specify a label to be included in file name and HTTP file name suggestions.')
    print('       components: Specify the orientation of the synthetic seismograms as a list of any combination of:')
    print('          Z(vertical),N(north),E(east),R(radial),T(transverse).')
    print('          Default: ZNE(except ak135f_1s: Z)')
    print('       units: displacement, velocity, acceleration.(The length unit is meters.)')
    print('       sample_interval: Specify the sampling interval in seconds. The default varies by model.')
    print('       kernel_width: Specify the width of the sinc kernel used for resampling to requested sample')
    print('                     interval, relative to the original sampling rate. Default: 12.')
    print('       amplitude_scale. Default: 1.(The default amplitude length unit is meters.)')
    print('   -h or --help  Help.')

def opt():
    source     = ''
    receiver   = ''
    begintime  = ''
    endtime    = ''
    model      = 'iasp91_2s'
    format_out = 'format=saczip&'
    misc_ops   = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"S:R:D:M:F:O:h",["help"])
    except:
        print("Invalid Argument.")
        Usage()
        sys.exit(1)
    if sys.argv[1:] == []:
        Usage()
        sys.exit(1)

    for op, value in opts:
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
                mech     = value[1:].split(',')[2].split('/')
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
#                    Usage()
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
                endtime = 'endtime=' + se[0] + '&'
            elif len(se) == 2:
                begintime = 'starttime=' + se[0] + '&'
                endtime = 'endtime=' + se[1] + '&'
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
            for ss in value.split('+')[1:]:
                if ss[0].lower() == 'l':
                    label = 'label='+ss[1:]+'&'
                elif ss[0].lower() == 'c':
                    components = 'components='+ss[1:]+'&'
                elif ss[0].lower() == 'u':
                    unit_value = ss[1:]
                    if ('D', 'dis', 'displacement').count(unit_value):
                        units = 'units=displacement&'
                    elif ('V', 'vel', 'velocity').count(unit_value):
                        units = 'units=velocity&'
                    elif ('A', 'acc', 'acceleration').count(unit_value):
                        units = 'units=acceleration&'
                    else:
                        print("No Units: "+unit_value+'.The units are set to be velocity.')
                        units = 'units=velocity&'
                elif ss[0].lower() == 's':
                    sample_interval = ss[1:]
                    try:
                        float(sample_interval)
                    except:
                        print("Sample interval must be in float")
                        sys.exit(1)
                    dt = 'dt=' + sample_interval + '&'
                elif ss[0].lower() == 'k':
                    try:
                        int(ss[1:])
                    except:
                        print("Kernel width must be in integer")
                        sys.exit(1)
                    kernel_width = 'kernelwidth='+ss[1:]+'&'
                elif ss[0].lower() == 'a':
                    try:
                        float(ss[1:])
                    except:
                        print("Scale must be in float")
                    amplitude_scale = 'scale='+ss[1:]+'&'
                else:
                    print("Error parameters in \"-O\"")
                    sys.exit(1)
            misc_ops = label+components+units+dt+kernel_width+amplitude_scale
        elif op in ('-h', '--help'):
            Usage()
            sys.exit(1)
    return source, receiver, begintime, endtime, model, format_out, misc_ops

def main():
    source, receiver, begintime, endtime, model, format_out, misc_ops = opt()
    synthetics = Syngines(source, receiver, begintime, endtime, model, format_out, misc_ops)
#    synthetics = Syngines('Source Options','Receiver Options','Data Range Options','Model','Format','Misc Options').download()
    synthetics.download()

if __name__ == '__main__':
    main()
