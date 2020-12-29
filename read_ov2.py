'''Read ov2 files by GPS manufactor TomTom.

The ov2 file specification interpreted from:
https://www.tomtom.com/lib/doc/ttnavsdk3_manual.pdf
'''

import argparse
import os, io, shutil


def bytes2coord(x):
    ''' Convert bytes to coordinate. WGS84 coordinates in decimal degrees (DD)'''
    return float(int.from_bytes(x, byteorder='little', signed=True)/100000)


def bytes2str(x):
    return x.decode()


# Input argument parser
parser = argparse.ArgumentParser()
parser.add_argument('file', help='ov2 file')
parser.add_argument('-o', '--output_file', help='Output file')
args = parser.parse_args()

# open ov2 file
fp = open(args.file, 'rb')

# output buffer
outbuf = io.StringIO()

try:
    while True:

        buf = fp.read(1)

        if not buf:
            break

        record_type = int.from_bytes(buf, byteorder='little')
        record_size = int.from_bytes(fp.read(4), byteorder='little')


        if record_type == 0: # "Deleted record" (unidentified content)
            fp.seek( record_size - 5 + fp.tell() )


        elif record_type == 1: # "Skipper record"
            record_long_w = bytes2coord( fp.read(4) )
            record_lati_s = bytes2coord( fp.read(4) )
            record_long_e = bytes2coord( fp.read(4) )
            record_lati_n = bytes2coord( fp.read(4) )


            # convert 'skipper record' position
            if record_long_w > 0:
                record_long = -1 * record_long_w
            else:
                reocrd_long = record_long_e

            if record_lati_s > 0:
                record_lati = -1 * record_long_s
            else:
                record_lati = record_lati_n


            outbuf.write('{},{},""'.format(record_long, record_lati))


        elif record_type == 2: # "Simple poi record"

            record_long = bytes2coord( fp.read(4) )
            record_lati = bytes2coord( fp.read(4) )

            name_size = record_size-4*3-1-1
            record_name = bytes2str( fp.read( name_size) )

            # forward zero terminated record byte
            fp.seek(1 + fp.tell())

            outbuf.write('{},{},"{}"'.format(record_long, record_lati,
                record_name) +os.linesep)


        elif record_type == 3: # "Extended poi record"

            record_long = bytes2coord( fp.read(4) )
            record_lati = bytes2coord( fp.read(4) )

            name_size = record_size-4*3-1-1
            record_name_id_extra = bytes2str( fp.read( name_size ) ).split(sep=b'\x00')
            record_name = record_name_id_extra[0]
            record_id = record_name_id_extra[1]
            record_extra = record_name_id_extra[2]

            # forward zero terminated record byte
            fp.seek(1 + fp.tell())

            outbuf.write('{},{},"{} - {} {}"'.format(record_long, record_lati,
                record_name, record_id, record_extra) + os.linesep)


        else:
            raise RuntimeError('Invalid record type in ov2 file')


    # Rewind outbuf for output
    outbuf.seek(0)

    # write to file or stdout
    if args.output_file:
        with open(args.output_file, 'wt') as fo:
            print('Writes locations to file "{}"'.format(args.output_file))
            shutil.copyfileobj(outbuf, fo)

    else:
        print(outbuf.read())


except Exception as err:

    print(err)

    # Display output buffer what has been read
    print('Read from "{}":'.format(args.file))
    outbuf.seek(0)
    print(outbuf.read())

    raise SystemExit('Invalid ov2 file')


finally:
    fp.close()
    outbuf.close()

exit(0)
