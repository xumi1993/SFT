#!/usr/bin/env python
"""
Download timeseries data by 'URL Builder: timeseries v.1'
"""
import sys
from util import Timeseries


def main():
#    print(Timeseries('IU','ANMO','00','BHZ','2010-02-27T06:30:00','2010-02-27T10:30:00','miniseed')._format)
    download = Timeseries('IU','ANMO','00','BHZ','2010-02-27T06:30:00','2010-02-27T10:30:00','miniseed').download()
#    download = Timeseries('IU','ANMO','00','BHZ','2010-02-27T06:30:00','2010-02-27T10:40:00','miniseed').download()

if __name__ == '__main__':
    main()
