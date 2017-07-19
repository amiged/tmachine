#!/usr/bin/env python3
import os
from datetime import datetime
import time

# YYYYMMDD_HH_MM_SS
def get_filename_frame(basedir, str_datetime):
    cell = list(str_datetime)
    str_YYYYMMDD = ''.join(cell[0:8])
    str_HH = ''.join(cell[9:11])
    str_MM = ''.join(cell[12:14])
    str_SS = ''.join(cell[15:17])
    dirname = basedir + str_YYYYMMDD + "/" + str_HH
    if os.path.exists(dirname) != True:
        os.makedirs(dirname)
    ret = dirname + "/" + str_datetime+".jpg"
    ret = ret.replace(' ','')
    return ret


def get_filename_frame_simple(basedir, fname):
    dirname = basedir
    if os.path.exists(dirname) != True:
        os.makedirs(dirname)
    ret = dirname + fname
    ret = ret.replace(' ','')
    return ret


if __name__ == '__main__':
    while(True):
        tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S')
        fname = get_filename_frame('../work/', tnow)
        print (fname)
        time.sleep(0.5)
