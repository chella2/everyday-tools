# everyday-tools
The repository [everyday-tools](https://github.com/chella2/everyday-tools) contains tools for creating and reading ov2 file for TomTom navigation devices. There is also a tool to convert positions of CNG/LPG gas station at [www.energigas.se](www.energigas.se) to CSV. The tools requires Python 3.x



## energigas2csv.py
Convert json formatted GPS locations to CSV (Comma Separated Value). The webpage [www.energigas.se](www.energigas.se) provides GPS locations of gas fueling stations (CNG, LNG/LBG) in a json format. In order to import those locations, data must be reformatted for most satellite navigation devices. Many GPS devices uses a specific format, which in most cases can be convertet to from a CSV-file.



## read_ov2.py
Read ov2 files by GPS manufactor TomTom and outputs as CSV (Comma Separated Value).



## create_ov2.py
Create ov2-file from a CSV-file. Each row in the input CSV must be a location using the format 'longitude,latitude,"Name"'. The longitude and latitude must be in WGS84 coordinates using decimal degrees (DD).



# Related information

## Creating POI set for TomTom GPS
Instructions making a POI set https://www.tomtom.com/lib/doc/TomTomTips/index.html?poi_set_using_makeov2.htm
