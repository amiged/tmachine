#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import cv2

drawing = False
mode = True
ix,iy = -1,-1

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('Push')
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            print ('Drawing...')
            if mode == True:
                pass
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)
        else:
            pass
    elif event == cv2.EVENT_LBUTTONUP:
        print ('Up')
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),2)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)

if '__main__' == __name__ :
    img = np.zeros((512,512,3), np.uint8)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)
    
    while(1):
        cv2.imshow('image',img)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break

    cv2.destroyAllWindows()
