#!/usr/bin/env python3
# ./mov.py <fps> <start_number>
import sys


if __name__ == '__main__':
	 args = sys.argv
	 assert len(args) == 3
	 fps          = int(args[1])
	 start_number = int(args[2])
	 cmd = "ffmpeg -r %d -start_number %d -i ../conv/%%08d.jpg -vcodec libx264 -pix_fmt yuv420p -r %d tmp.mp4"% (fps, start_number, fps)
	 print (cmd)
