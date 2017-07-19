#!/usr/bin/env python3
# ----------------------------------------------------------------------
# BBox-Label-Tool
#1
#231 204 403 455
# ----------------------------------------------------------------------
# darknet 
#0 0.49531250000000004 0.6864583333333333 0.26875 0.5229166666666667
# ----------------------------------------------------------------------
import glob

def convert(size, box):
    dw = (size[0])
    dh = (size[1])
    x = (box[0] + box[2])/2.0
    y = (box[1] + box[3])/2.0
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x/dw
    w = w/dw
    y = y/dh
    h = h/dh
    return (x,y,w,h)


def _convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[2])/2.0 - 1
    y = (box[1] + box[3])/2.0 - 1
    w = box[2] - box[0]
    h = box[3] - box[1]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

flist = glob.glob("../data4bbox/Labels/777/image*.txt")
flist.sort()

for fname in flist:
    with open(fname, "r") as fd:
        lines = fd.readlines()
        l = lines[1].replace('\n','')
        box_str = l.split(' ')
        box = []
        for v in box_str:
            box.append(float(int(v)))

        size = [640.0, 480.0]
        x, y, w, h = convert(size, box)

        if False:
        #if True:
            x0 = box[0]
            y0 = box[1]
            x1 = box[2]
            y1 = box[3]
            x = (x0 + x1)/2.0/size[0]
            y = (y0 + y1)/2.0/size[1]


        #print(fname, lines[1], box, x, y, w, h)
        print("%1.17f %1.17f %1.17f %1.17f " %(x, y, w, h))

    
