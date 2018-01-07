#!/usr/bin/env python
# encoding: utf-8

import argparse
import os
from datetime import datetime


def get_time():
    stamp = datetime.now()
    stamp_str = stamp.isoformat(' ', timespec='seconds')
    return stamp_str


def main():
    parser = argparse.ArgumentParser(description='Create a post.')
    parser.add_argument('title', type=str, nargs='+',
                        help='The title of the new post')
    parser.add_argument('-t', type=str, nargs='+', dest='tags',
                        help='The tags of the new post')
    args = parser.parse_args()
    stamp_str = get_time()
    post_file = stamp_str.split()[0]
    title_str = ' '.join(str(part) for part in args.title)
    post_file += '-' + '-'.join(str(part) for part in args.title) + '.md'
    tag_str = ', '.join(str(tag) for tag in args.tags)

    with open(os.path.join('blog/_posts', post_file), 'w') as post_handle:
        str_stream = '---\nlayout: post'
        str_stream += '\ntitle: ' + title_str
        str_stream += '\nmodified: ' + stamp_str
        str_stream += '\ntags: [' + tag_str + ']'
        str_stream += '\ndescription:\n---\n'
        post_handle.write(str_stream)


if __name__ == '__main__':
    main()
