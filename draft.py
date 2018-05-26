import os
from datetime import datetime

def main():
    stamp_str = str(datetime.now())
    post_file_name = '{}-newpost.md'.format(stamp_str.split()[0])

    with open(os.path.join('blog/_posts', post_file_name), 'w') as post_handle:
        str_stream = '---\nlayout: post'
        str_stream += '\ntitle: '
        str_stream += '\nmodified: ' + stamp_str
        str_stream += '\ntags: []'
        str_stream += '\ndescription:\n---\n'
        post_handle.write(str_stream)


if __name__ == '__main__':
    main()
