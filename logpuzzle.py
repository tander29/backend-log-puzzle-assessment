#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what puzzle_path puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns puzzle_path list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    url = 'http://' + filename[(filename.find('_') + 1):]
    all_lines = []
    puzzles_list = []
    with open(filename) as f:
        all_lines = f.readlines()
    for line in all_lines:
        puzzle_path = re.search(r'\S+(puzzle)\S+', line)
        if puzzle_path:
            puzzles_list.append(url + puzzle_path.group(0))
    if 'place' in filename:
        return sorted(set(puzzles_list), key=lambda x: x[(x.rfind('-')+1):])
    return sorted(set(puzzles_list))


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if os.path.isdir(dest_dir):
        return
    os.mkdir(dest_dir)
    os.chdir(dest_dir)
    images = []
    for n, path in enumerate(img_urls):
        urllib.urlretrieve(path, 'img{}.jpg'.format(n))
        images.append('img{}.jpg'.format(n))
        print(path)
    with open('index.html', 'w') as f:
        f.write('<html><body>\n')
        for image in images:
            f.write('<img src="{}">'.format(image))
        f.write('\n')
        f.write('</body></html>')
    print(os.getcwd())


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
