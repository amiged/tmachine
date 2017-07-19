#!/usr/bin/env python3
import numpy as np
import cv2
from datetime import datetime
import mkdir
import sys

def put_text(image, text):
    font_size = 1.0
    font_type = cv2.FONT_HERSHEY_PLAIN
    font_color = (0xf, 0xf, 0xff)
    cv2.putText(image, text, (460, 15), font_type, font_size, font_color)
    


if (__name__ == '__main__'):
    argv = sys.argv
    devid = int(argv[1])
    log_base = '../log/'
    cap = cv2.VideoCapture(devid)

    cap_width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap_fps    = cap.get(cv2.CAP_PROP_FPS)

    print(cap_width, "x", cap_height, ":", cap_fps)

    tnow0 = datetime.now().strftime('%Y%m%d_%H_%M_%S') # ('%Y%m%d_%H_%M_%S_%f')

    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)

        tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S')
        if(tnow != tnow0):
            put_text(frame, tnow)
            ofname = mkdir.get_filename_frame('../log/', tnow)
#            cv2.imwrite(ofname, frame)
            print(ofname, ": TEST on devid=%d"%devid)
            tnow0 = tnow
 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Done.")
