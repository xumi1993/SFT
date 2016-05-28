# Units of SFT 
#
# Author: Mijian Xu, Tao Gou, Haibo Wang
#

import re
import sys
from os.path import join
from progressive.bar import Bar
try:
    import urllib.request as rq
except:
    import urllib as rq

def bar(response, chunk_size=8192):
   if response.headers['Content-Length'] == None:
      print("No response of server")
      sys.exit(1)
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
   return chunk_all,itype

class Stations:
   '''
   Based on URL Builder: station v.1
   '''

   url = 'http://service.iris.edu/fdsnws/station/1/'

   def __init__(self, lalo_label, net_label, sta_label, loc_label, cha_label, date_label):
       self.urllink = ('%squery?%s%s%s%s%s%sformat=text' %(self.url, lalo_label,
           net_label, sta_label, loc_label, cha_label, date_label))

   def download(self):
      try:
         self.response = rq.urlopen(self.urllink)
      except:
         print('Something wrong for unknown reason!')
         sys.exit(1)

   def output(self):
      html = self.response.read().decode()
      print(html.strip())

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
    url = 'http://service.iris.edu/irisws/timeseries/1/'

    def __init__(self,network,station,location,channel,starttime,endtime,output):
#        if output not in self._format:
#            raise ValueError('Output format(\'%s\') is invalid!' %output)
        self.urllink = '%squery?net=%s&sta=%s&cha=%s&start=%s&end=%s&output=%s&loc=%s' % (self.url,network,station,channel,starttime,endtime,output,location)

    def download(self):
        download_url = self.urllink
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
            with open(filename,'wb') as f:
                f.write(data)
        else:
            with open(filename,'w') as f:
                f.write(data)

class Traveltime:
    """
    Based on 'URL Builder: traveltimes v.1'
    """

    url = 'http://service.iris.edu/irisws/traveltime/1/'

    def __init__(self, model_label, phases_label, evdp_label, nohder_label, dist_label):
        self.urllink = ('%squery?%s%s%s%s%s' % (self.url, model_label, phases_label, evdp_label, nohder_label, dist_label))

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

    def __init__(self, network, station, location, channel, istime, timeinfo, ispz):
        self.network = network
        self.station = station
        self.channel = channel
        self.location = location
        self.ispz = ispz
        if ispz:
            self.url = 'http://service.iris.edu/irisws/sacpz/1/'
        else:
            self.url = 'http://service.iris.edu/irisws/resp/1/'
        if istime == 1:
            self.urllink = ('%squery?net=%s&sta=%s&loc=%s&cha=%s&time=%s' % (self.url, network, station,
                location, channel, timeinfo[0].strftime('%Y-%m-%dT%H:%M:%S')))
        elif istime == 2:
            self.urllink = ('%squery?net=%s&sta=%s&loc=%s&cha=%s&starttime=%s&endtime=%s' % (self.url, network, station, 
                location, channel, timeinfo[0].strftime('%Y-%m-%dT%H:%M:%S'), timeinfo[0].strftime('%Y-%m-%dT%H:%M:%S')))
        else:
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
#        data,itype = bar(response)
        print("Downloading %s..." % filename)
        data = response.read().decode()
        with open(join(path, filename), 'w') as f:
            f.write(data)

