#!/usr/bin/env python3
#Time-stamp: <2017-06-03 03:06:20 hamada>
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir
import aieye_find
import time
import sys


if (__name__ == '__main__'):
    basedir = '../log/'
    if (len(sys.argv) > 1 ):
        basedir = sys.argv[1]
    
    iflist = [] 
    for fname in aieye_find.find(basedir, '*.jpg'):
        iflist.append(fname)

    iflist.sort()
    ni = len(iflist)
    i = 0
    i_fp = 0.0
    i_delta = 1
    i_scale = 60.0
    speed_state = 0

    #    for i, fname in enumerate(iflist):
    while( i < ni) :
        fname = iflist[i]

        #print (fname, i, ni, i/ni)
        image = cv2.imread(fname)
        cv2.imshow("play.py", image)

        key = cv2.waitKey(1) & 0xFF
        if key != 255:  print (key, "%d/%d"% (i, ni))

        if key  == 114:           i_fp = 0.  # r

        if key  == ord('q'): break
        if key  == 97:            i_fp -= 1.  # d
        if key  == 100:           i_fp += 1.  # a
        if key  == 81:            i_fp -= 5.  # <-
        if key  == 83:            i_fp += 5.  # ->
        if key  == 86:            i_fp += 30. # Up
        if key  == 85:            i_fp -= 30. # Down
        if key  == 82:            i_fp += 300. # PgDn
        if key  == 84:            i_fp -= 300. # PgUp

        if key  == ord(' '): 
            if 0 != speed_state: 
                i_delta = 0
                speed_state = 0
            else:
                i_delta = 1
                speed_state = 1
            print ("i_delta:", i_delta)
            print ("speed_state:", speed_state)


        if key  == 226: # R_SHIFT
            if 0 == speed_state:
                i_delta = int(i_scale/10.)
                speed_state = 1
            elif 1 == speed_state:
                i_delta = int(i_scale)
                speed_state = 2
            elif 2 == speed_state:
                i_delta = int(i_scale*10.)
                speed_state = 3
            elif 3 == speed_state:
                i_delta = int(i_scale*100.)
                speed_state = 4
            elif 4 == speed_state:
                i_delta = 1
                speed_state = 0
            else:
                i_delta = 1
                speed_state = 0
            print ("i_delta:", i_delta)
            print ("speed_state:", speed_state)

        if key  == ord('+'): 
            i_delta *= 2
            print ("i_delta:", i_delta)

        if key  == ord('-'): 
            i_delta = int(i_delta / 2)
            if i_delta < 1: i_delta = 1 
            print ("i_delta:", i_delta)

        #----------------------------------
        i_fp += i_delta/i_scale
        if i_fp < 0.0 :  i_fp = 0.0
        if i_fp >= float(ni): i_fp = float(ni) -1.0
        i = int(i_fp)

    cv2.destroyAllWindows()
