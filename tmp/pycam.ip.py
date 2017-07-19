#!/usr/bin/env python3
#Time-stamp: <2017-06-11 19:19:34 hamada>
import cv2
import urllib.request
import numpy as np
import argparse
from datetime import datetime
import mkdir

class DroidCam(object):
    def __init__(self):
        self.droidapp = 'IP Webcam'
        self.ipadr  = '192.168.43.1'
#        self.ipadr  = '192.168.42.129'
#        self.ipadr  = '133.45.9.162'
        self.port  = '3389'
        self.stream = -1
        self.URL = -1
        self.image = -1
    def get_stream(self):
        stub = ''
        if (self.droidapp == 'DroidCam'):
            stub = '/mjpegfeed?960x720'
        elif (self.droidapp == 'IP Webcam'):
            stub = '/video?dummy=param.mjpg'
        else:
            stub = '/mjpegfeed?640x480'

        url = 'http://'+self.ipadr+':'+self.port + stub

        print ('URL: ', url)
        self.URL = url
        self.stream = urllib.request.urlopen(self.URL)
        return (self.stream)

    def get_stream_jpg(self):
        stub = '/shot.jpg'
        url = 'http://'+self.ipadr+':'+self.port + stub
        print ('URL: ', url)
        self.URL = url
        self.stream = urllib.request.urlopen(self.URL)
        return (self.stream)

    def get_jpg(self):
        stub = '/shot.jpg'
        url = 'http://'+self.ipadr+':'+self.port + stub
        urlObj = urllib.request.urlopen(url)
        print ('URL: ', url, urlObj.getcode())
        ofname = '/dev/shm/now.jpg'
        with open(ofname, "wb") as file:
            file.write(urlObj.read())
        self.image = cv2.imread(ofname)
        return (self.image)
        
    def set_focus(self):
        stub = '/focus'
        url = 'http://'+self.ipadr+':'+self.port + stub
        print ('focus: ', url)
        urlObj = urllib.request.urlopen(url)
        

class State(object):
    def __init__(self):
        self.is_record = False
        self.drawing = False
        self.posi0 = [-1,-1]
        self.posi1 = [-1,-1]
        self.image = -1
        self.image_size = [-1, -1] # [height, width]
        self.image_orig = -1
        self.class_num = 777
        self.image_num = 1

    def draw_rect(self):
        # print ("posi0, posi1: ", self.posi0, self.posi1)
        cv2.rectangle(self.image, (self.posi0[0], self.posi0[1]), (self.posi1[0], self.posi1[1]), (0, 255, 0), 1)

    def draw_text(self):
        if(self.is_record):
            font = cv2.FONT_HERSHEY_TRIPLEX # cv2.FONT_HERSHEY_PLAIN
            font_size = 0.8
            text = "<<%d>>"% (self.image_num)
            color = (0x0, 0x0, 0xBF)
            px = int(self.image_size[1]/2)
            py = 30
            cv2.putText(self.image, text,(px, py), font, font_size, color)

state = State()

def mouse_event(event,x,y,flags,param):
    global state

    if x < 0: x = 0
    if y < 0: y = 0
    if x >= state.image_size[1]: x = state.image_size[1] - 1
    if y >= state.image_size[0]: y = state.image_size[0] - 1


    if event == (cv2.EVENT_LBUTTONDOWN):
        state.posi0[0] = x0 = state.posi1[0]
        state.posi0[1] = y0 = state.posi1[1]
        state.posi1[0] = x
        state.posi1[1] = y
        print ("Rect: (%d, %d) - (%d, %d)"%(x0, y0, x, y) )


def put_text(image, text):
    font_size = 1.0
    font_type = cv2.FONT_HERSHEY_PLAIN
    font_color = (0xf, 0xf, 0xff)
    cv2.putText(image, text, (5, 15), font_type, font_size, font_color)


if (__name__ == '__main__'):

    droidcam = DroidCam()
#    stream = droidcam.get_stream()

    parser = argparse.ArgumentParser(description = "description goes here")
    parser.add_argument("--devid", type=int, help = "set device id", required=False)
    args = parser.parse_args()
    devid = 0
    if args.devid:
        devid = int(args.devid)
        print ("set devid = ", devid)

    while True:
        frame = droidcam.get_jpg()
        state.image_orig = frame.copy()
        state.image      = frame.copy()
        state.image_size[0], state.image_size[1] = frame.shape[:2]
        state.draw_rect()
        state.draw_text()
        cv2.imshow('droidcam',state.image)
        tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S_%f')
        if True:
            basedir = '../log.ipcam.%d/'% (devid)
            ofname = mkdir.get_filename_frame(basedir, tnow)
            put_text(state.image, tnow)
            cv2.imwrite(ofname, state.image)
            print(ofname)
            tnow0 = tnow
            state.image_num += 1

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        if ( (key == ord(' ')) or 
             (key == 34) or # Muhenkan
             (key == 35) or # Henkan
             (key == 39) or # katakana
             (key == 10)    # Enter
        ):
            state.is_record = not (state.is_record)
        if key == ord('f'): droidcam.set_focus()


    cv2.destroyAllWindows()
    print("Done.")

