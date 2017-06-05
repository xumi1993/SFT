# SFT
Seismic fetch tools based on IRIS Web Services

## Dependencies
* Python 2.7.x or Python 3.x.x

## Download
```
git clone https://github.com/xumi1993/SFT.git
```

## Update
```shell
cd /path/to/SFT
git pull
```

## Inclusion
* get_events.py: Fetch catalog from GCMT, NEIC or ISC
* get_station.py: List of stations in metadata
* get_traveltime.py: Travel times and ray parameters for seismic phases using a 1-D spherical earth model
* get_resp: Instrument response information evaluated from IRIS metadata
* get_timeseries: Time series data in miniSEED format
* get_synthetics.py: An API of IRIS Synthetics Engine (Syngine) service, which provides custom tailored synthetic seismograms
