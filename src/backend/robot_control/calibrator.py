import time

import robot_control_http as rch

# Calibration sequence moves the robot arm to the four corners of the operating area
# For each corner, an image is taken to later map image coordinates to robot coordinates



def calibrate(token):
    rch.initialize(token)
    time.sleep(15)
    rch.move(475, 0, 200, -180, 0, -180, token)
    time.sleep(15)
    rch.move(350, 300, 200, -180, 0, -180, token)
    time.sleep(15)
    rch.move(600, 300, 200, -180, 0, -180, token)
    time.sleep(15)
    rch.move(600, -300, 200, -180, 0, -180, token)
    time.sleep(15)
    rch.move(350, -300, 200, -180, 0, -180, token)
    time.sleep(15)
    rch.initialize(token)
