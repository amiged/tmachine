#!/usr/bin/env python3
import numpy as np
import cv2
from datetime import datetime


def put_text(image, text):
    font_size = 1.0
    font_type = cv2.FONT_HERSHEY_PLAIN
    font_color = (0xff, 0xf, 0xff)
    cv2.putText(image, text, (460, 15), font_type, font_size, font_color)
    

image = cv2.imread("/tmp/tmp.jpg")

tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S') # ('%Y%m%d_%H_%M_%S_%f')
put_text(image, tnow)
cv2.imshow('test', image)


while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

print("Done.")
