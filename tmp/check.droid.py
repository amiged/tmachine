#!/usr/bin/env python3
#Time-stamp: <2017-06-10 01:52:29 hamada>
import cv2
import urllib.request
import numpy as np

#stream=urllib.request.urlopen('http://133.45.9.162:3389/mjpegfeed?640x480')        # for DroidCam
stream=urllib.request.urlopen('http://192.168.101.160:3389/video?dummy=param.mjpg') # for IP Webcam

bytes = b''
while True:
    raw = stream.read(1024)
    bytes += raw
    #print (bytes)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.imshow('droidcam',image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break

cv2.destroyAllWindows()

