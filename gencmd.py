#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
git remote add origin git@github.com:amiged/NAME.git
git push -u origin master
'''

import datetime as dt
import glob
import uuid
import random

def read_bitmap(fname='/home/hamada/git/tmachine/map.txt'):
    bitmap = [ ] 
    with open(fname, 'r') as fh:
        lines = fh.readlines()
        for line in lines:
            line = line.rstrip('\n')
            ss = list(line)
            bitmap.extend(ss)

    return bitmap

def gen_cmd(tstr, src_files, dst_files):
    # secure_unique_id = uuid.uuid4().hex
    index_src = random.randint(0, len(src_files)-1) % len(src_files)
    index_dst = random.randint(0, len(dst_files)-1) % len(dst_files)
    code_name_src = src_files[index_src]
    code_name_dst = dst_files[index_dst]

    cmd  = "sudo date -s '%s';\n" % (tstr)
    cmd += "date > %s;\n" % (code_name_dst)
    cmd += "cat %s >> %s;\n" % (code_name_src, code_name_dst)
    cmd += "git add .;\n"
    cmd += "~/git/tmachine/commit.py |bash - ;\n"
    print (cmd, end='')

def draw_git(t0, cnt, src_files, dst_files):
    if cnt == 0: return
    t = t0
    for i in range(cnt):
        t = t + dt.timedelta(seconds=random.randint(300, 600)) # randomly adjust first/next commit time for the day # max stride = 10min (600sec)
        t_str =  t.strftime('%m/%d %H:%M:%S %Y')
        gen_cmd (t_str, src_files, dst_files)


def get_src_files():
    src_files = []
    src_files.extend(glob.glob('/home/hamada/git/tmachine/tmp/*'))
    src_files.sort()
    return src_files

def get_dst_files(nmax=77):
    files = []
    for i in range(0, nmax):
        fname = uuid.uuid4().hex
        files.append(fname)
    random.shuffle(files)
    return files

if __name__ == "__main__":
    random.seed()
    src_files = get_src_files()
    dst_files = get_dst_files()
    bmap = read_bitmap()
    #print (bmap)

    t0_str = '2014-12-28 19:21:17' # Sunday
    t0_str = '2008-01-06 19:21:17' # Sunday
    t0_str = '2005-12-25 19:21:17' # Sunday
    
    t = dt.datetime.strptime(t0_str, '%Y-%m-%d %H:%M:%S')
    print ("sudo date -s '%s'" % t0_str)

    print ("git init")
    print ("\n")

    for i in bmap:
        draw_git(t, int(i), src_files, dst_files)
        t = t + dt.timedelta(days=1)

