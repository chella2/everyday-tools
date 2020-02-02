import os
import json
import requests
import argparse
import io, shutil

'''
Convert json data from www.energigas.se to CSV
'''

# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output-file', help='Output file')
group_url_or_file = parser.add_mutually_exclusive_group(required=True)
group_url_or_file.add_argument('-c', '--cng-gas', action='store_true', help='CNG gas locations from www.energigas.se')
group_url_or_file.add_argument('-l', '--lng-gas', action='store_true', help='LNG/LBG gas locations from www.energigas.se')
group_url_or_file.add_argument('-u', '--url', type=str, help='Provide own URL to data')
group_url_or_file.add_argument('-f', '--file', type=str, help='Provide local file with data')
args = parser.parse_args()


if args.cng_gas:
    url = 'https://www.energigas.se/api/GasStations/get?pageId=3601'
    json_data = requests.get(url).text

elif args.lng_gas:
    url = 'https://www.energigas.se/api/GasStations/get?pageId=6341'
    json_data = requests.get(url).text

elif args.url:
    url = args.url
    json_data = requests.get(url).text

elif args.file:
    with open(args.file, 'r') as fp:
        json_data = fp.read()


# load json data into python dict
data = json.loads(json_data)

# buffer for output data
buf = io.StringIO()

try:

    for poi in data:
        buf.write('{},{},"{} - {}"'.format(poi['Longitude'], poi['Latitude'], poi['Name'], poi['Street'].capitalize()) + os.linesep)

    # Rewind output buffer before output
    buf.seek(0)

    if args.output_file:
        with open(args.file, 'wt') as fp:
            print('Writing content to "{}"'.format(args.output_file))
            shutil.copyfileobj(buf, fp)

    else:
        print(buf.read())


except Exception:
    print('Bad formatted json input')

finally:
    buf.close()


exit(0)
