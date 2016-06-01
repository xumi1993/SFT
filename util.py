# Units of SFT 
#
# Author: Mijian Xu, Tao Gou, Haibo Wang @ Nanjing University
#
# History: 2016-05-07 Init codes, Tao Gou
#          2016-05-27 Add class of get_traveltime, Haibo Wang
#          2016-05-28 Add class of get_resp, Mijian Xu
#          2016-06-01 Add class of Syngines, Haibo Wang
#

import re
import sys
from os.path import join
from progressive.bar import Bar
from datetime import datetime
try:
    import urllib.request as rq
except:
    import urllib as rq

def get_time(timestr):
    if len(timestr.split("T")) == 1:
        time = datetime.strptime(timestr, "%Y-%m-%d")
    elif len(timestr.split("T")) == 2:
        time = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S")
    else:
        print("Wrong datetime options")
        sys.exit(1)
    return time

def bar(response, chunk_size=8192):
#    if response.headers['Content-Length'] == None:
#        print("No response of server")
#        sys.exit(1)
    total_size = response.headers['Content-Length'].strip()
    total_size = int(total_size)
    cycle = int(total_size/chunk_size)+1
    bytes_so_far = 0

    MAX_VALUE = 100

    bar = Bar(max_value=MAX_VALUE, num_rep="percentage", fallback=True)
    
    bar.cursor.clear_lines(2)
    bar.cursor.save()
    for i in range(cycle):
        chunk = response.read(chunk_size)
        if i == 0:
            if type(chunk) != str:
                chunk_all = b''
                itype = 'bytes'
            else:
                chunk_all = ''
                itype = 'str'
        bytes_so_far += len(chunk)
        chunk_all += chunk
        percentage = int(bytes_so_far*100/total_size)
        bar.cursor.restore()
        bar.draw(value=percentage)
        print('%dbyte/%dbyte' %(bytes_so_far,total_size))
    return chunk_all, itype


class Stations:
    '''
    Based on URL Builder: station v.1
    '''

    url = 'http://service.iris.edu/fdsnws/station/1/'

    def __init__(self, lalo_label, net_label, sta_label, loc_label, cha_label,\
            dateb_label, datee_label, level_label, comment_label):
        self.comment_label = comment_label
        self.level_label = level_label
        self.urllink = ('%squery?%s%s%s%s%s%s%s%s%sformat=text' %(self.url, lalo_label,
                net_label, sta_label, loc_label, cha_label,dateb_label, datee_label, level_label, comment_label))

    def download(self):
        try:
            self.response = rq.urlopen(self.urllink)
        except:
            print('Something wrong for unknown reason!')
            sys.exit(1)

    def output(self):
        self.html = self.response.read().decode().strip()
        print(self.html)

    def gmt_script(self):
        with open("station.gmt", "w") as f:
            f.write("#!/usr/bin/sh\n")
            f.write("ps=stations.ps\n")
            f.write("gmt pscoast -Rg -J0/10i -Bxa30g30 -Bya30g30 -Dl -A1000 -G200 -W0.4p -K > $ps\n")
            f.write("gmt psxy -R -J -O -W0.2p -Gred3 -St0.08i >> $ps << eof\n")
            if self.comment_label == "includecomments=false&":
                lines = self.html.split("\n")
            else:
                lines = self.html.split("\n")[1:]
            if self.level_label == '' or level_label == "level=station&":
                idxlat = 2
                idxlon = 3
            elif self.level_label == "level=channel&":
                idxlat = 4
                idxlon = 5
            else:
                print("The level must be \"station\" (default) or \"channel\"")
                return
            for station in lines:
                station = station.strip()
                lat = station.split("|")[idxlat]
                lon = station.split("|")[idxlon]
                f.write("%s %s\n" % (lon, lat))
            f.write("eof\n")
                
class Events:
   '''
   Based on 'URL Builder: event v.1'
   '''

   url = 'http://service.iris.edu/fdsnws/event/1/'

   def __init__(self, lalo_label, dep_label, mag_label, cata_label, date_label):
       self.urllink = ('%squery?format=text&%s%s%s%s%s' %(self.url, lalo_label, 
                         dep_label, mag_label, cata_label, date_label))[:-1]

   def download(self):
      try:
         self.response = rq.urlopen(self.urllink)
      except:
         print('Something wrong for unknown reason!')
         sys.exit(1)

   def output(self):
      evt_lst = self.response.readlines()
      for evt in evt_lst:
         evt = evt.decode().strip()
         if evt[0] == '#':
            continue
         print(evt)


class Timeseries:
    '''
    Download timeseries data with information such as network,station,location,channel,starttime,endtime and output
    '''

#    _format = ['miniseed', 'ascii1', 'ascii2', 'audio', 'plot', 'saca', 'sacbb', 'sacbl']
#    url = 'http://service.iris.edu/irisws/timeseries/1/'
    url = 'http://service.iris.edu/fdsnws/dataselect/1/'
    
    def __init__(self, network, station, location, channel, starttime, endtime, output):
        self.network = network
        self.station = station
        self.channel = channel
        self.location = location
        self.starttime = starttime
        self.endtime = endtime
#        if output not in self._format:
#            raise ValueError('Output format(\'%s\') is invalid!' %output)
        self.urllink = '%squery?net=%s&sta=%s&loc=%s&cha=%s&start=%s&end=%s' % \
                       (self.url, network, station, location, channel, starttime, endtime)

    def download(self, path):
        download_url = self.urllink
        print(download_url)
        filename = join(path, "%s.%s.%s.%s.%s.%s.mseed" % \
                (self.network, self.station, self.location, self.channel, self.starttime, self.endtime))
        print("Downloading data to %s......" % filename)
        rq.urlretrieve(download_url, join(path, filename))
'''
        try:
            response = rq.urlopen(download_url)
            #   print(response.getcode())
        except:
           print('Something wrong for unknown reason!')
           sys.exit(1)
        filename = response.headers['Content-Disposition'].split('=')[1]
        data,itype = bar(response)
#        data = response.read()
        if itype == 'bytes':
            with open(join(path, filename),'wb') as f:
                f.write(data)
        else:
            with open(join(path, filename),'w') as f:
                f.write(data)
'''

class Traveltime:
    """
    Based on 'URL Builder: traveltimes v.1'
    """

    url = 'http://service.iris.edu/irisws/traveltime/1/'

    def __init__(self, model_label, phases_label, evdp_label, nohder_label, dist_label):
        self.urllink = ('%squery?%s%s%s%s%s' % (self.url, model_label, phases_label,
                                                evdp_label, nohder_label, dist_label))

    def download(self):
        try:
            self.response = rq.urlopen(self.urllink)
        except:
            print("Something wrong for unknown reason!")
            sys.exit(1)

    def output(self):
        phs = self.response.read().decode()
        print(phs)

class Response:
    """
    Based on "resp v.1" and "sacpz v.1"
    """

    def __init__(self, network, station, location, channel, timeinfo, ispz):
        self.network = network
        self.station = station
        self.channel = channel
        self.location = location
        self.ispz = ispz
        if ispz:
            self.url = 'http://service.iris.edu/irisws/sacpz/1/'
        else:
            self.url = 'http://service.iris.edu/irisws/resp/1/'
        if len(timeinfo) == 2:
            self.urllink = ('%squery?net=%s&sta=%s&loc=%s&cha=%s&time=%s' % (self.url, network, station,
                location, channel, timeinfo[0].strftime('%Y-%m-%dT%H:%M:%S')))
        elif len(timeinfo) == 1:
            self.urllink = ('%squery?net=%s&sta=%s&loc=%s&cha=%s&starttime=%s&endtime=%s' % (self.url, network, station, 
                location, channel, timeinfo[0].strftime('%Y-%m-%dT%H:%M:%S'), timeinfo[0].strftime('%Y-%m-%dT%H:%M:%S')))
        elif timeinfo == []:
            self.urllink = ('%squery?net=%s&sta=%s&loc=%s&cha=%s' % (self.url, network, station, 
                location, channel))

    def download(self, path):
        try:
            response = rq.urlopen(self.urllink)
        except:
            print("Something wrong for unknown reason!")
            sys.exit(1)
        if self.ispz:
            filename = "SAC_PZs_%s_%s_%s_%s" % (self.network, self.station, self.channel, self.location)
        else:
            filename = response.headers.get_filename()
        print("Downloading %s..." % filename)
        data = response.read().decode()
        with open(join(path, filename), 'w') as f:
            f.write(data)
            
class Syngines:
    """
    Based on "syngines v.1"
    """

    url = 'http://service.iris.edu/irisws/syngine/1/'

    def __init__(self,source,receiver,data_range,model,format_out,misc_ops):
        self.urllink = '%squery?%s%s%s%s%s%snodata=404' % (self.url,source,receiver,data_range,model,format_out,misc_ops)

    def download(self):
        download_url = self.urllink
        try:
            response = rq.urlopen(download_url)
        except:
            print('Something Wrong for Unknown Reason!')
            sys.exit(1)
        filename = response.headers['Content-Disposition'].split('=')[1]
        data,itype = bar(response)
        if itype == 'bytes':
            with open(filename,'wb') as f:
                f.write(data)
        else:
            with open(filename,'w') as f:
                f.write(data)
