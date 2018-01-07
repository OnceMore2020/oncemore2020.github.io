#!/usr/bin/env python
# encoding: utf-8

import os

def compile():
    username = os.getcwd().split('/')[2]
    homedir = os.path.join('/home', username)
    repodir = os.path.join(homedir, 'blogbuild')
    gitbook_dir = os.path.join(repodir,'ruminations')
    gitbook_src_dir = os.path.join(gitbook_dir, 'src')

    # use gitbook-cli to compile each book
    for subdir in os.listdir(gitbook_src_dir):
        subpath = os.path.join(gitbook_src_dir, subdir)
        target_dir = os.path.join(gitbook_dir, subdir)
        os.chdir(subpath)
        os.system('gitbook init')
        os.system('gitbook install')
        os.system('gitbook build')
        os.system('mv _book ' + target_dir)

    # use jekyll to build site
    os.chdir(repodir)
    os.system('jekyll build')


if __name__ == '__main__':
    compile()
