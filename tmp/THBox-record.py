#!/usr/bin/env python3
#Time-stamp: <2017-06-04 15:57:17 hamada>
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir

class State(object):
    def __init__(self):
        self.is_record = False

if (__name__ == '__main__'):
    state = State()

    parser = argparse.ArgumentParser(description = "description goes here")
    parser.add_argument("--devid", type=int, help = "set device id", required=False)
    args = parser.parse_args()
    devid = 0
    if args.devid:
        devid = int(args.devid)
        print ("set devid = ", devid)


    log_base = '../log/'
    cap = cv2.VideoCapture(devid)

    cap_width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_fps    = cap.get(cv2.CAP_PROP_FPS)

    print(cap_width, "x", cap_height, ":", cap_fps)


    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('camera: %d'%(devid), frame)

        tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S_%f')
        if(state.is_record):
            basedir = '../log.%d/'% (devid)
            ofname = mkdir.get_filename_frame(basedir, tnow)
            cv2.imwrite(ofname, frame)
            print(ofname, "devid = %d"%devid)
            tnow0 = tnow

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        if key == ord(' '): state.is_record = not (state.is_record)


    cap.release()
    cv2.destroyAllWindows()

    print("Done.")
