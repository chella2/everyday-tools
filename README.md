# everyday-tools
Tools to help and simplify everyday life


# Tool content
Requires Python 3.x

## energigas2csv.py
This script converts locations for www.energigas.se to CSV (Comma Separated Value). The website www.energigas.se provides locations of gas fueling stations (CNG, LNG/LBG) in json format. In order to import those locations, data must be reformatted for most satellite navigation devices. Many GPS devices uses a specific format, which can be convertet to from a CSV-file.


## read_ov2.py
This script read ov2 files by GPS manufactor TomTom and outputs as CSV (Comma Separated Value).


## create_ov2.py
This script creates ov2-file from a CSV. Each row in the input CSV must be a location using the format 'longitude,latitude,"Name"'. The longitude and latitude must be in WGS84 coordinates using decimal degrees (DD).



# Other information

## Creating POI set for TomTom GPS
Instructions making a POI set https://www.tomtom.com/lib/doc/TomTomTips/index.html?poi_set_using_makeov2.htm
