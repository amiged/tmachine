all:
	./pycam.py |tee log.txt


clean:
	rm -rf ../conv
	mkdir ../conv
	rm -f *~ .*~
	rm -rf __pycache__

c: clean

conv:
	rm -rf ../conv
	mkdir ../conv
	./gen_cmd.py > xxx
	bash ./xxx


mov:
	./mov.py 1 0


0.mov: 
	rm -f out.mp4
	ffmpeg -r 1 -start_number 0 -i ../conv/%08d.jpg -vcodec libx264 -pix_fmt yuv420p -r 1 out.mp4

r: run

run:
	./mpycam.py

run3:
	./pycam.py --devid=0 &
	./pycam.py --devid=1 &
	./pycam.py --devid=2 &

kill:
	killall python3
	killall pycam.py

clog: clean
	rm -rf ../log* ../data4bbox ../data4darknet ../conv
	rm -rf ./tmp.mp4
