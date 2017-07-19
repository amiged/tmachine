#!/usr/bin/env python3
#Time-stamp: <2017-06-01 03:19:59 hamada>
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir

def get_ndev():
    ndev = 0
    devid = []
    for i in range(0, 10):
        c = cv2.VideoCapture(i)
        if c.isOpened():
            ndev = ndev + 1
            devid.append(i)
        c.release()

    print ("devid = ", devid)
    return ndev

def isOpened(cap):
    ret = True
    for c in cap:
        ret = ret and c.isOpened()
    return ret


def put_text(image, text):
    font_size = 1.0
    font_type = cv2.FONT_HERSHEY_PLAIN
    font_color = (0xaf, 0xff, 0xaf)
    #    cv2.putText(image, text, (460, 15), font_type, font_size, font_color)
    cv2.putText(image, text, (10, 15), font_type, font_size, font_color)

if (__name__ == '__main__'):
    ndev = get_ndev()
    log_base = '../log/'
    cap = []
    for i in range(ndev):
        cap.append(cv2.VideoCapture(i))

    # -- swap cap --
    if False:
        cap_tmp = cap[0]
        cap[0] = cap[2]
        cap[2] = cap_tmp


    cap_width  = cap[0].get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap[0].get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_fps    = cap[0].get(cv2.CAP_PROP_FPS)

    print(cap_width, "x", cap_height, ":", cap_fps)
    size = (int(cap_width/2), int(cap_height/2))

    tnow0 = datetime.now().strftime('%Y%m%d_%H_%M_%S') # ('%Y%m%d_%H_%M_%S_%f')

    while(isOpened(cap)):
        frame = [0] * ndev
        for (i, fm) in enumerate(frame):
            ret, fm = cap[i].read()
            smallimg = cv2.resize(fm, size)
            if False: cv2.imshow('camera: %d'%(i), smallimg)
            frame[i] = smallimg

        # ----------------------------------------------------------------
        frame_height, frame_width = frame[0].shape[:2]

        nwx = 3
        nwy = int(1.0+(ndev-1)/3.0)

        image = np.zeros((frame_height * nwy, frame_width*nwx, 3), dtype=np.uint8)
        # image = np.zeros((frame_height, frame_width*ndev, 3), dtype=np.uint8)

        # --- ROI ---
        for (i, fm) in enumerate(frame):
            sx = frame_width * (i%nwx)
            sy = frame_height * int(i/nwx)
            ex = frame_width * (i%nwx+1)
            ey = frame_height * int(1+i/nwx)
            image[sy:ey,sx:ex] = fm

        cv2.imshow(__file__, image)

        tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S_%f')
        if(tnow != tnow0):
            put_text(image, tnow)
            basedir = '../log/'
            ofname = mkdir.get_filename_frame(basedir, tnow)
            cv2.imwrite(ofname, image)
            print(ofname)
            tnow0 = tnow

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for (i, fm) in enumerate(frame):
        cap[i].release()

    cv2.destroyAllWindows()

    print("Done.")
