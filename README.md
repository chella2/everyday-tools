# everyday-tools
Tools to help and simplify everyday life


# Contents
The tools requires Python 3.x

## energigas2csv.py
Convert json formatted GPS locations to CSV (Comma Separated Value). The website www.energigas.se provides GPS locations of gas fueling stations (CNG, LNG/LBG) in a json format. In order to import those locations, data must be reformatted for most satellite navigation devices. Many GPS devices uses a specific format, which can be convertet to from a CSV-file.


## read_ov2.py
Read ov2 files by GPS manufactor TomTom and outputs as CSV (Comma Separated Value).


## create_ov2.py
Create ov2-file from a CSV-file. Each row in the input CSV must be a location using the format 'longitude,latitude,"Name"'. The longitude and latitude must be in WGS84 coordinates using decimal degrees (DD).


## photo_collector.py
Recursivly collect photos and images from a source path to target path. Only copies photos that are not already at target directory. Images that are coopied from the source are sorted in target directory using structure Year/Month. The image date is based on Exif metadata (DateTimeOriginal) if available, otherwise most recent metadata change (Unix) or time of creation (Windows).

This script requires package exifread. See section 'Setup virtual environment'


# Related information

## Creating POI set for TomTom GPS
Instructions making a POI set https://www.tomtom.com/lib/doc/TomTomTips/index.html?poi_set_using_makeov2.htm


# Setup virtual environment

* Create a virtual python environment called 'env'

    virtualenv env

* Activate the virtual environment

    source env/bin/activate

* Install required packages

    pip install -r requirements.txt
