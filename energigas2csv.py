'''
Convert json data from www.energigas.se with gas fueling stations to CSV.
The output data is using the format 'longitud,latitude,"Name"'.
'''

import os
import json
import urllib.request
import argparse
import io, shutil



# input argument parser
parser = argparse.ArgumentParser(description='''Convert json formatted GPS positions to CSV.
    GPS positions for CNG or LPG gas fueling stations are retrieved from www.energigas.se. GPS
    positions can also be used from provided url or local file.
    The output data is using format 'longitud,latitude,"Name"'.''')


parser.add_argument('-o', '--output-file', help='Output file')

group_url_or_file = parser.add_mutually_exclusive_group(required=True)


group_url_or_file.add_argument('-c', '--cng-gas',
                                action='store_true',
                                help='CNG gas locations at www.energigas.se')

group_url_or_file.add_argument('-l', '--lng-gas',
                                action='store_true',
                                help='LNG/LBG gas locations at www.energigas.se')

group_url_or_file.add_argument('-u', '--url',
                                type=str,
                                help='URL to json data')

group_url_or_file.add_argument('-f', '--file',
                                type=str,
                                help='local file with json data')

args = parser.parse_args()


if args.cng_gas:
    url = 'https://www.energigas.se/api/GasStations/get?pageId=3601'
    json_data = urllib.request.urlopen(url).read().decode()

elif args.lng_gas:
    url = 'https://www.energigas.se/api/GasStations/get?pageId=6341'
    json_data = urllib.request.urlopen(url).read().decode()

elif args.url:
    url = args.url
    json_data = urllib.request.urlopen(url).read().decode()

elif args.file:
    with open(args.file, 'r') as fp:
        json_data = fp.read()


# load json data into python dict
data = json.loads(json_data)

# buffer for output data
buf = io.StringIO()

try:

    for poi in data:
        buf.write('{},{},"{} - {}"'.format(poi['Longitude'], poi['Latitude'],
            poi['Name'], poi['Street'].capitalize()) + os.linesep)

    # Rewind output buffer before output
    buf.seek(0)

    if args.output_file:
        with open(args.output_file, 'wt') as fp:
            print('Storing CSV file "{}"'.format(args.output_file))
            shutil.copyfileobj(buf, fp)

    else:
        print(buf.read())


except Exception as err:
    print(err)

finally:
    buf.close()


exit(0)
