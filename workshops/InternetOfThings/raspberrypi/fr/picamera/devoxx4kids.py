import numpy as np
import subprocess
import sys
import termios
import tty
import config
import picamera
import picamera.array
import time

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return ch

def timelaps(path, image_template, wait_time, resolution, video_name):
	result = subprocess.call(["avconv", "-f", "image2", "-r", wait_time, "-i", "%s/%s" % (path, image_template), "-r", wait_time, "-s", resolution, "%s/%s" % (path, video_name)])

def getArrayImage(camera):
		camera.exposure_mode = 'auto'
		camera.resolution = (128, 80)
                camera.awb_mode = 'auto'
		time.sleep(0.5)
		with picamera.array.PiRGBArray(camera) as stream:
			camera.capture(stream, format='rgb', use_video_port=False)
			return stream.array


def getStreamImage(isDay):
    # Capture an image stream to memory based on daymode
    with picamera.PiCamera() as camera:
        time.sleep(0.5)
        camera.resolution = (128, 80)
        with picamera.array.PiRGBArray(camera) as stream:
            print "isDay %s" % isDay
            if isDay:
                camera.exposure_mode = 'auto'
                camera.awb_mode = 'auto'
                camera.capture(stream, format='rgb', use_video_port=False)
            else:
                # Take Low Light image
                # Set a framerate of 1/6fps, then set shutter
                # speed to 6s
                camera.framerate = Fraction(1, 6)
                camera.shutter_speed = nightMaxShut
                camera.exposure_mode = 'off'
                camera.iso = nightMaxISO
                # Give the camera a good long time to measure AWB
                # (you may wish to use fixed AWB instead)
                time.sleep( nightSleepSec )
                camera.capture(stream, format='rgb')
            return stream.array


def checkForMotion(data1, data2, threshold):
    # Find motion between two data streams based on sensitivity and threshold
    motionDetected = False
    pixChanges = (np.absolute(data1-data2)>threshold).sum()/3
    print "> %d  - %d" % (pixChanges, threshold)

    return pixChanges
#    if pixChanges > sensitivity:
#        motionDetected = True
#    if motionDetected:
#        dotCount = showDots(motionMaxDots + 2)
#        logging.info("Found Motion - threshold=%s  sensitivity=%s changes=%s", threshold, sensitivity, pixChanges)
#    return motionDetected
