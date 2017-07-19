#!/usr/bin/env python3
#Time-stamp: <2017-06-03 00:45:13 hamada>
import cv2
import glob
import aieye_find
from datetime import datetime

iflist = [] 
for fname in aieye_find.find('../log.0/20170602/18/', 'sss_*.jpg'):
    iflist.append(fname)

iflist.sort()
i = 0
index = 0

for fname in iflist:
    fname_src = fname # fname.replace('../log/', "/mnt/data/work/bak/log/")
    fname_dst = fname.replace('sss_', 'CanonG1X_')
    if( i % 1 == 0):  # every 30 sec 
#        cmd =  "ln -s " + fname_src + " " + "../conv/%08d.jpg" % (index)
        cmd =  "mv " + fname_src + " " + fname_dst
        print (cmd, "; echo '%d/%d: %s'; "%(i, len(iflist), fname_src) )
        index += 1
    i += 1
