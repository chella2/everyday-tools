'''Create ov2 files for GPS manufactor TomTom.

The ov2 file specification interpreted from:
https://www.tomtom.com/lib/doc/ttnavsdk3_manual.pdf
'''

import argparse
import os, io, shutil
import csv


def str2coord(x):
    '''Convert input string to integer coordinate'''
    return int(float(x)*100000)


# Input argument parser
parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='CSV file')
parser.add_argument('-o', '--output_file', help='Output ov2-file', required=True)
args = parser.parse_args()

# open csv file
csv_file = open(args.csv_file, 'rt')
csv_reader = csv.reader(csv_file, delimiter=',')

# output buffer
outbuf = io.BytesIO()

try:
    for row in csv_reader:

        # debug information
        #print('{} {} {}'.format(str2coord(row[0]), str2coord(row[1]), row[2] ) )

        # Set record type '2' (Simple poi record)
        outbuf.write( int(2).to_bytes(1, byteorder='little') )

        # record length in bytes (type + length + coordinates + name + nullbyte)
        rec_len = 1 + 4 + 2*4 + len(row[2].encode()) +1
        outbuf.write( rec_len.to_bytes(4, byteorder='little') )

        # longitude
        outbuf.write( str2coord(row[0]).to_bytes(4, byteorder='little', signed=True) )

        # latitude
        outbuf.write( str2coord(row[1]).to_bytes(4, byteorder='little', signed=True) )

        # Name
        outbuf.write( row[2].encode() )

        # null byte
        outbuf.write('\x00'.encode() )


    # Rewind output buffer
    outbuf.seek(0)

    # write content to file
    with open(args.output_file, 'bw') as fp:
        print('Saving file: "{}"'.format(args.output_file))
        shutil.copyfileobj(outbuf, fp)


except Exception as err:
    raise SystemExit(err)

finally:
    csv_file.close()
    outbuf.close()


exit(0)
