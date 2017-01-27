import picamera
import picamera.array
import devoxx4kids as d4k
import io
import time

path = "/home/pi/d4k/album"
pictureNumber = 0
videoNumber = 0

default_camera_resolution = (1024, 768)
motion_camera_resolution = (128, 80)

effectsList = ["none", "negative", "sketch"]
effectNumber = 0

with picamera.PiCamera() as camera:
    camera.resolution = default_camera_resolution
    camera.start_preview()

    while True:
        char = d4k.getch()
        if char is None:
            pass
        elif (char == "x"):
            camera.stop_preview()
            break
        elif (char == "f"):
            effectNumber = ( effectNumber + 1 ) % len(effectsList)
            camera.image_effect = effectsList[effectNumber]
        elif (char == "p"):
            pictureNumber = pictureNumber + 1
            camera.capture("%s/image%02d.jpg" % (path, pictureNumber))
            print "Capturing image image%s.jpg" % pictureNumber
        elif (char == "v"):
            videoNumber = videoNumber + 1
            print "Start recording video video%02d.h264..." % videoNumber
            camera.start_recording("%s/video%02d.h264" % (path, videoNumber))
            time.sleep(5)
            camera.stop_recording()
            print "Stop recording video."
        elif (char == "t"):
            videoNumber = videoNumber + 1
            print "Compute timelaps video video%02d.avi..." % videoNumber
            d4k.timelaps(path, "image%02d.jpg", "1", "1280x720", "video%02d.avi" % videoNumber)
            print "Timelaps complete."
        elif (char == "m"):
            print "Start motion detection"
            camera.stop_preview()
            camera.resolution = motion_camera_resolution 

            ref_image = d4k.getArrayImage(camera)
            while True:
                current_image = d4k.getArrayImage(camera)
                if d4k.checkForMotion(ref_image,current_image):
                    pictureNumber = pictureNumber + 1
                    camera.resolution = default_camera_resolution
                                camera.capture("%s/image%02d.jpg" % (path, pictureNumber))
                                print "MOTION DETECTED: Capturing image image%s.jpg" % pictureNumber    
                    camera.resolution = motion_camera_resolution
                ref_image = current_image
                char = d4k.getch()
                if (char == "m"):
                    print "Exit motion detection"
                    camera.resolution = default_camera_resolution
                    camera.start_preview()
                    break;

