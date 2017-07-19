#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir
import aieye_find
import time
import sys

class_num = 1 # annotate number for class: 001: hamada
drawing = False
posi0 = [-1,-1]
posi1 = [-1,-1]
image_size = [-1, -1] # [height, width]

def mouse_event(event,x,y,flags,param):
    global posi0, posi1, drawing

    if x < 0: x = 0 
    if y < 0: y = 0 
    if x >= image_size[1]: x = image_size[1] - 1
    if y >= image_size[0]: y = image_size[0] - 1


    if event == cv2.EVENT_LBUTTONDOWN:
        print ('Push')
        drawing = True
        posi0[0] = x
        posi0[1] = y


    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            print ("Drawing... (%d, %d)" % (x, y))
        else:
            pass
    elif event == cv2.EVENT_LBUTTONUP:
        print ('Up')
        drawing = False
        cv2.rectangle(image, (posi0[0],posi0[1]), (x,y), (0,255,0), 1)
        posi1[0] = x
        posi1[1] = y

def save_data(image_dbg, image_orig, fnum):
    global class_num, posi0, posi1
    basedir = '../data4bbox/'
    fname_body = "image_%04d" % fnum

    # save image_orig (for Images/)
    fname = fname_body + ".jpg"
    basedir_images = basedir+"Images/%03d/"%(class_num)
    ofname_images = mkdir.get_filename_frame_simple(basedir_images , fname)
    print (ofname_images)
    cv2.imwrite(ofname_images, image_orig)

    # save image_dbg (for Debug/)
    fname = fname_body + ".jpg"
    basedir_dbg = basedir+"Debug/%03d/"%(class_num)
    ofname_dbg  = mkdir.get_filename_frame_simple(basedir_dbg , fname)
    print (ofname_dbg)
    cv2.imwrite(ofname_dbg, image_dbg)

    # save labes
    fname = fname_body + ".txt"
    basedir_labels = basedir+"Labels/%03d/"%(class_num)
    ofname_labels  = mkdir.get_filename_frame_simple(basedir_labels , fname)
    print (ofname_labels)
    bbox_posi = []
    bbox_posi.append(min(posi0[0], posi1[0]))
    bbox_posi.append(min(posi0[1], posi1[1]))
    bbox_posi.append(max(posi0[0], posi1[0]))
    bbox_posi.append(max(posi0[1], posi1[1]))
    with open(ofname_labels, "w") as file:
        file.write("1\n")
        file.write("%d %d %d %d\n" % (tuple(bbox_posi)))

if '__main__' == __name__:
    basedir = '../log/'
    if (len(sys.argv) > 1 ):
        basedir = sys.argv[1]
    
    iflist = [] 
    for fname in aieye_find.find(basedir, '*.jpg'):
        iflist.append(fname)

    iflist.sort()
    ni = len(iflist)
    i = 0

    #    for i, fname in enumerate(iflist):
    while( i < ni) :
        fname = iflist[i]
        print (fname, "%d/%d (%1.3f)"%(i, ni, i/ni))

        image_orig = cv2.imread(fname, cv2.IMREAD_COLOR)
        image = image_orig.copy()
        image_size[0], image_size[1] = image.shape[:2]
        is_next = False
        while (not is_next):
            cv2.imshow("THBox-annon.py", image)
            cv2.namedWindow("THBox-annon.py", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("THBox-annon.py", mouse_event)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                save_data(image, image_orig, i)
                is_next = True
            if key  == 83:  # ->
                is_next = True
            if key  == 81:  # <-
                i = i - 2
                is_next = True
            if key == ord('r'): # Reset
                i = i - 1
                is_next = True
            if key  == ord('q'): 
                i = ni
                break
        i = i+1

    cv2.destroyAllWindows()





    
