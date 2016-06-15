#!/usr/bin/env python
# Fetch timeseries by events
#
# Author: Mijian Xu
#
# History: 2016-06-07, Init code, Mijian Xu
#
import re
import sys
import getopt
from os.path import isfile, realpath, dirname, isdir, join, exists
from os import makedirs
sys.path.append(dirname(dirname(realpath(__file__))))
from util import Events, get_time, Stations, Traveltime, Timeseries, Response
from datetime import timedelta


def Usage():
    print("Usage: ./fetchdata_events.py")

def opt():
    lalo_label = ''
    dep_label = ''
    mag_label = ''
    cata_label = 'catalog=GCMT&'
    network = ''
    station = '*'
    location = '*'
    channel = 'BH?'
    outpath = './'
    phase_begin = []
    phase_end = []
    stalist = []
    istimeb = False
    istimee = False
    islist = False
    isoutsta = False
    isresp = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "R:D:b:e:C:H:M:P:n:s:l:c:S:o:r:")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)
    if not sys.argv[1:]:
        print("No argument is found")
        Usage()
        sys.exit(1)
    ops = [op for op, value in opts]
    if not ("-b" in ops and "-e" in ops):
        print("\"-b\" and \"-e\" must be specified.")
        sys.exit(1)
    if "-n" in ops and "-S" in ops:
        print("-n is incompatible with specified station list")
        sys.exit(1)

    for op, value in opts:
        if op == "-R":
            lon1 = value.split("/")[0]
            lon2 = value.split("/")[1]
            lat1 = value.split("/")[2]
            lat2 = value.split("/")[3]
            lalo_label = 'minlat=' + lat1 + '&maxlat=' + lat2 + '&minlon=' + lon1 + '&maxlon=' + lon2 + '&'
        elif op == "-D":
            lat = value.split("/")[0]
            lon = value.split("/")[1]
            dist1 = value.split("/")[2]
            dist2 = value.split("/")[3]
            lalo_label = 'lat=' + lat + '&lon=' + lon + '&maxradius=' + dist2 + '&minradius=' + dist1 + '&'
        elif op == "-H":
            dep1 = value.strip("/")[0]
            dep2 = value.strip("/")[1]
            dep_label = 'mindepth=' + dep1 + '&maxdepth=' + dep2 + '&'
        elif op == "-b":
            begintime = get_time(value)
        elif op == "-e":
            endtime = get_time(value)
        elif op == "-C":
            cata_label = 'catalog=' + value + '&'
        elif op == "-M":
            mag1 = value.split("/")[0]
            mag2 = value.split("/")[1]
            if len(value.split("/")) == 2:
                mag_label = 'minmag=' + mag1 + '&maxmag=' + mag2 + '&'
            else:
                mtype = value.split("/")[2]
                mag_label = 'minmag=' + mag1 + '&maxmag=' + mag2 + '&magtype=' + mtype + '&'
        elif op == "-P":
            evtb_label = value.split('/')[0]
            evte_label = value.split('/')[1]
            try:
                phase_begin.append(float(evtb_label))
                istimeb = 1
            except:
                phase_begin.append(re.search('\w+', evtb_label).group())
                phase_begin.append(float(re.search('\W\d+', evtb_label).group()))
            try:
                phase_end.append(float(evte_label))
                istimee = 1
            except:
                phase_end.append(re.search('\w+', evte_label).group())
                phase_end.append(float(re.search('\W\d+', evte_label).group()))
        elif op == "-n":
            network = value
        elif op == "-s":
            station = value
        elif op == "-l":
            location = value
        elif op == "-c":
            channel = value
        elif op == "-S":
            islist = True
            sub_op = value.split("+")
            if len(sub_op) != 1 and len(sub_op) != 2:
                print("Error options in -S")
                sys.exit(1)
            if isfile(sub_op[0]):
                with open(sub_op[0], 'r') as f:
                    stalist = f.readlines()
            else:
                print("No such list file")
                sys.exit(1)
            if len(sub_op) == 2:
                if sub_op[1] == "s":
                    isoutsta = True
        elif op == "-o":
            outpath = value
            if not isdir(outpath):
                print("No such directory")
                sys.exit(1)
        elif op == "-r":
            if value == '':
                isresp = 1
            elif value == '+p':
                isresp = 2
            else:
                print("Error sub-option in -r")
                sys.exit(1)
        else:
            Usage()
            sys.exit(1)
    return lalo_label, dep_label, begintime, endtime, cata_label, mag_label, phase_begin, phase_end, istimeb, istimee, \
            network, station, location, channel, stalist, islist, outpath, isoutsta, isresp

def main():
    lalo_label, dep_label, begintime, endtime, cata_label, mag_label, phase_begin, phase_end, istimeb, istimee, \
    network, station, location, channel, stalist, islist, path, isoutsta, isresp = opt()
    if (not islist) and (istimeb or istimee):
        print("Cannot specify time range by phases when station info was specified in command line")
        sys.exit(1)
    date_label = "start=" + begintime.strftime("%Y-%m-%dT%H:%M:%S") + \
                 "&end=" + endtime.strftime("%Y-%m-%dT%H:%M:%S") + "&"
    events = Events(lalo_label, dep_label, mag_label, cata_label, date_label, "", False)
    events.download()
    evt_lst = events.out_events
    if evt_lst == []:
        print("No event in this date range")
        sys.exit(1)
    for evt in evt_lst:
        evt = evt.strip()
        origin_time = get_time(evt.decode().split('|')[1])
        evla = float(evt.decode().split('|')[2])
        evlo = float(evt.decode().split('|')[3])
        evdp = float(evt.decode().split('|')[4])
        evmagtp = evt.decode().split('|')[9]
        evmag = evt.decode().split('|')[10]
        if not isoutsta:
            outpath = join(path, "evt.%s.%s%s" % (origin_time.strftime("%Y%m%d"), evmagtp, evmag))
            if not exists(outpath):
                makedirs(outpath)
        if islist:
            for sta in stalist:
                sta = sta.strip()
                lstnet = "net=" + sta.split()[0] + "&"
                lststa = "sta=" + sta.split()[1] + "&"
                stainfo = Stations('', lstnet, lststa, '', '', date_label, '', False, '', '')
                stainfo.download()
                stla = stainfo.out_station[0].decode().strip().split('|')[2]
                stlo = stainfo.out_station[0].decode().strip().split('|')[3]
                if isoutsta:
                    outpath = join(path, sta.split()[0]+'.'+sta.split()[1])
                    if not exists(outpath):
                        makedirs(outpath)
                if istimeb:
                    evt_begin = origin_time + timedelta(seconds=phase_begin[0])
                else:
                    out_label = "noheader=true&mintimeonly=true&traveltimeonly=true&"
                    dist_label = 'evloc=[' + str(evla) + ',' + str(evlo) + ']&staloc=[' + stla + ',' + stlo + ']'
                    phase_label = "phases=" + phase_begin[0] + "&"
                    beg_tt = Traveltime("model=iasp91&", phase_label, "evdepth=" + str(evdp) + "&", out_label,
                                        dist_label)
                    beg_tt.download()
                    ttime = float(beg_tt.phs.strip().split()[0])
                    evt_begin = origin_time+timedelta(seconds=ttime)+timedelta(seconds=phase_begin[1])
                if istimee:
                    evt_end = origin_time + timedelta(seconds=phase_end[0])
                else:
                    out_label = "noheader=true&mintimeonly=true&traveltimeonly=true&"
                    dist_label = 'evloc=[' + str(evla) + ',' + str(evlo) + ']&staloc=[' + stla + ',' + stlo + ']'
                    phase_label = "phases=" + phase_end[0] + "&"
                    end_tt = Traveltime("model=iasp91&", phase_label, "evdepth=" + str(evdp) + "&", out_label,
                                        dist_label)
                    end_tt.download()
                    ttime = float(end_tt.phs.strip().split()[0])
                    evt_end = origin_time + timedelta(seconds=ttime) + timedelta(seconds=phase_end[1])
                if evt_begin > evt_end:
                    print("start-time great than end-time in event %s %s.%s" % (origin_time.strftime("%Y%m%d"), lstnet, lststa))
                    continue
                Timeseries(sta.split()[0], sta.split()[1], sta.split()[2], sta.split()[3],
                           evt_begin.strftime("%Y-%m-%dT%H:%M:%S"),
                           evt_end.strftime("%Y-%m-%dT%H:%M:%S")).download(outpath)
                if not isoutsta:
                    if isresp == 1:
                        Response(sta.split()[0], sta.split()[1], sta.split()[2], sta.split()[3], [evt_begin, evt_end],
                                 False).download(outpath)
                    elif isresp == 2:
                        Response(sta.split()[0], sta.split()[1], sta.split()[2], sta.split()[3], [evt_begin, evt_end],
                                 True).download(outpath)
                    else:
                        continue
        else:
            evt_begin = origin_time + timedelta(seconds=phase_begin[0])
            evt_end = origin_time + timedelta(seconds=phase_end[0])
            Timeseries(network, station, location, channel,
                       evt_begin.strftime("%Y-%m-%dT%H:%M:%S"),
                       evt_end.strftime("%Y-%m-%dT%H:%M:%S")).download(outpath)
            if isresp == 1:
                Response(network, station, location, channel, [evt_begin, evt_end],
                         False).download(outpath)
            elif isresp == 2:
                Response(network, station, location, channel, [evt_begin, evt_end],
                         True).download(outpath)
            else:
                continue

    if islist and isoutsta:
        for sta in stalist:
            outpath = join(path, sta.split()[0]+'.'+sta.split()[1])
            sta = sta.strip()
            if isresp == 1:
                Response(sta.split()[0], sta.split()[1], sta.split()[2], sta.split()[3], [evt_begin, evt_end],
                         False).download(outpath)
            elif isresp == 2:
                Response(sta.split()[0], sta.split()[1], sta.split()[2], sta.split()[3], [evt_begin, evt_end],
                         True).download(outpath)
            else:
                continue

if __name__ == '__main__':
    main()