import freenect
import cv2
import numpy as np
import pyglet
import time
from time import localtime, strftime
import datetime





# function to get RGB image from kinect
def get_video():
    array, _ = freenect.sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array

BASELINE_DEPTH = 80
#should be set to whatever value doesnt trigger the door opening
# function to get depth image from kinect
def get_depth(count):

    song = pyglet.media.load('Warning2.m4a')
    array, _ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    checker = 0
    for x in range(150, 350):
        for y in range (150, 350):
            if(array[x][y] >= BASELINE_DEPTH):
                checker += 1

    if checker >= (200*200)/2:

        stwing = (datetime.datetime.now().strftime("%X"))
        print ("Intruder detected at " + stwing)
        frame = get_video()

        song.play()
        time.sleep(3)

        cv2.imwrite("frame" + (datetime.datetime.now().strftime("%X") + ".jpg"  ), frame)
        time.sleep(2)
    return array


if __name__ == "__main__":
    count = 0
    while 1:
        depth = get_depth(count= count)
        count += 1

        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()