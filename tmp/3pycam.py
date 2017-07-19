#!/usr/bin/env python3
#Time-stamp: <2017-05-30 09:51:10 hamada>
import argparse
import numpy as np
import cv2
from datetime import datetime
import mkdir

def put_text(image, text):
    font_size = 1.0
    font_type = cv2.FONT_HERSHEY_PLAIN
    font_color = (0xaf, 0xdf, 0xf)
    #    cv2.putText(image, text, (460, 15), font_type, font_size, font_color)
    cv2.putText(image, text, (10, 15), font_type, font_size, font_color)

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description = "description goes here")
    parser.add_argument("--devid", type=int, help = "set device id", required=False)
    args = parser.parse_args()
    devid = 0
    if args.devid:
        devid = int(args.devid)
        print ("set devid = ", devid)

    log_base = '../log/'
    cap = []
    for i in range(3):
        cap.append(cv2.VideoCapture(i))

    # -- swap cap --
    if True:
        cap_tmp = cap[0]
        cap[0] = cap[2]
        cap[2] = cap_tmp


    cap_width  = cap[0].get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap[0].get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_fps    = cap[0].get(cv2.CAP_PROP_FPS)

    print(cap_width, "x", cap_height, ":", cap_fps)
    size = (int(cap_width/2), int(cap_height/2))

    tnow0 = datetime.now().strftime('%Y%m%d_%H_%M_%S') # ('%Y%m%d_%H_%M_%S_%f')

    while(cap[0].isOpened() and cap[1].isOpened() and cap[2].isOpened()):
        frame = [0,0,0]
        for (i, fm) in enumerate(frame):
            ret, fm = cap[i].read()
            smallimg = cv2.resize(fm, size)
            if False: cv2.imshow('camera: %d'%(i), smallimg)
            frame[i] = smallimg

        # ----------------------------------------------------------------
        frame_height, frame_width = frame[0].shape[:2]
        image = np.zeros((frame_height, frame_width*3, 3), dtype=np.uint8)

        for (i, fm) in enumerate(frame):
            sx = frame_width * i
            sy = 0
            ex = frame_width * (i+1)
            ey = frame_height
            image[sy:ey,sx:ex] = fm

        cv2.imshow('pycam', image)

        tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S')
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
