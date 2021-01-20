''' Recursivly collect photos and images from a source path to target path.

Note the following:
* Only images that are not already in the target directory are copied.
* Images copied to target will be sorted in directory structure: Year/Month.

'''

import os
import shutil
import mimetypes
import re
import hashlib
import pathlib
from datetime import datetime
import argparse
from pprint import pprint


import exifread
""" Some python EXIF packages
* PIL - old, not maintained anymore
* Pillow - PIL fork, libraries in c/c++
* exif  -
* exifread (repo name: exif-py)
* py3exiv2
* pyexiv2
"""



def image_files(path):
    ''' Returns a dictionary with image files at given path'''

    file_dict = dict()

    img_regex = re.compile(r'^image/')


    for root, dir, files in os.walk(path):

        for filename in files:

            file_path = os.path.join(root, filename)
            file_mime = mimetypes.guess_type(file_path)


            if re.match(img_regex, file_mime[0] or ''):

                with open(file_path, 'rb') as f:

                    file_chksum = hashlib.md5(f.read()).hexdigest()
                    tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')


                if 'EXIF DateTimeOriginal' in tags:
                    create_date = datetime.strptime(tags['EXIF DateTimeOriginal'].values,
                                                    '%Y:%m:%d %H:%M:%S')

                else:
                    fn = pathlib.Path(file_path)
                    create_date = datetime.fromtimestamp(fn.stat().st_ctime)


                file_dict[file_chksum] = {'path': file_path, 'date': create_date }

    return file_dict




# Input argument parser
parser = argparse.ArgumentParser()
parser.add_argument('source_dir', help='Source directory path')
parser.add_argument('target_dir', help='Target directory path')
parser.add_argument('-f', '--force', help='Do not prompt for confirmation', action='store_true')
parser.add_argument('-v', '--verbose', help='Enable verbosity', action='store_true')
args = parser.parse_args()



source_files = image_files(args.source_dir)

target_files = image_files(args.target_dir)

if args.verbose:
    print('{}Files found at source path: {}'.format(os.linesep, args.source_dir))
    pprint(source_files)
    print('{}Files found at target path: {}'.format(os.linesep, args.target_dir))
    pprint(target_files)


print('{} images files found in {}'.format(len(source_files), args.source_dir))
print('{} images files found in {}'.format(len(target_files), args.target_dir))


if not args.force:
    confirm_copy = input('Copy missing files to target? yes/no: ')

    if not confirm_copy == 'yes':
        raise SystemExit('Exits. You answer differ from yes')


copy_counter = 0

for chk_sum, img in source_files.items():

    if not chk_sum in target_files:

        year_taken= img['date'].strftime('%Y')
        month_taken= img['date'].strftime('%m_%B')

        target_path = os.path.join( args.target_dir,
                                    year_taken,
                                    month_taken,
                                    os.path.basename(img['path']))

        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copyfile(img['path'], target_path, follow_symlinks=False)
        shutil.copystat(img['path'], target_path, follow_symlinks=False)

        copy_counter += 1


print('{} files copied to {}'.format(copy_counter, args.target_dir))
