#!/usr/bin/env python3
import cv2
import glob
from datetime import datetime
import time 

while(True):
    tnow = datetime.now().strftime('%Y%m%d_%H_%M_%S_%f')
    print(tnow)

    with open(".tc~", "w") as file:
        file.write(tnow +"\n")

    time.sleep(3)
