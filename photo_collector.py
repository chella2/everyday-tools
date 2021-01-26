''' Recursivly collect photos and images from a source path to target path.

Note the following:
* Only images that are not already in the target directory are copied.
* Images copied to target will be sorted in directory structure: Year/Month.

Room for improvements:
* Status information while copying images to target
'''

import os
import shutil
import mimetypes
import re
import hashlib
import pathlib
from datetime import datetime
import argparse


import exifread
""" Some python EXIF packages
* PIL - old, not maintained anymore
* Pillow - PIL fork, libraries in c/c++
* exif  -
* exifread (repo name: exif-py)
* py3exiv2
* pyexiv2
"""



def find_images(path, verbose=False):
    ''' Returns a dict with image files at input path'''

    path_content = dict()

    img_regex = re.compile(r'^image/')


    for root, dir, files in os.walk(path):

        for filename in files:

            file_path = os.path.join(root, filename)
            file_mime = mimetypes.guess_type(file_path)


            if re.match(img_regex, file_mime[0] or ''):

                with open(file_path, 'rb') as fp:

                    file_chksum = hashlib.md5(fp.read()).hexdigest()

                    try:
                        tags = exifread.process_file(fp, stop_tag='EXIF DateTimeOriginal')

                    except:
                        tags = {}

                        if verbose:
                            print('exiftool failed on file {}'.format(file_path))



                try:
                    creation_date = datetime.strptime(tags['EXIF DateTimeOriginal'].values,
                                                    '%Y:%m:%d %H:%M:%S')

                except:

                    try:
                        date_match = re.match(r'^(?P<year>\d+)[:/](?P<month>\d+)[:/](?P<day>\d+)',
                                              tags['EXIF DateTimeOriginal'].values)

                        date_dict = date_match.groupdict()

                        creation_date = datetime(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))


                    except:
                        fn = pathlib.Path(file_path)
                        creation_date = datetime.fromtimestamp(fn.stat().st_mtime)


                path_content[file_chksum] = {'path': file_path, 'date': creation_date }


    return path_content




# Input argument parser
parser = argparse.ArgumentParser()
parser.add_argument('source_dir', help='Source directory path')
parser.add_argument('target_dir', help='Target directory path')
parser.add_argument('-f', '--force', help='Do not prompt for confirmation', action='store_true')
parser.add_argument('-v', '--verbose', help='Enable verbosity', action='store_true')

args = parser.parse_args()


print('Searching for images. This may take a while...')

source_files = find_images(args.source_dir, args.verbose)
target_files = find_images(args.target_dir, args.verbose)


print('{} images files found in source directory {}'.format(len(source_files), args.source_dir))
print('{} images files found in target directory {}'.format(len(target_files), args.target_dir))


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


        # ensure target file does not already exists
        img_root, img_ext = os.path.splitext(target_path)
        n = 0

        while os.path.exists(target_path):
            n += 1
            target_path = ''.join([img_root, '_' + str(n), img_ext])


        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copyfile(img['path'], target_path, follow_symlinks=False)
        shutil.copystat(img['path'], target_path, follow_symlinks=False)

        copy_counter += 1


print('{} files copied to {}'.format(copy_counter, args.target_dir))


with open(os.path.join(args.target_dir, 'photo_collector_log.txt'), 'a') as fp:

    for sha in target_files:
        fp.write(sha + '\n')
