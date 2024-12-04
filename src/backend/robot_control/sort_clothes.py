from backend.robot_control.robot_control_http import move, toggle, open_gripper, close_gripper
import numpy as np
from backend.utils.image_to_robot import get_robot_coordinates_of_basket_center
import time

def pick_up_cloth(token: str):
    open_gripper(token)
    time.sleep(1)
    move(450, 0, 15, -180, 0, -180, token) # Use coordinates of the cloth pile
    time.sleep(11)
    close_gripper(token)
    time.sleep(3)
    move(450, 0, 200, -180, 0, -180, token)
    time.sleep(6)

def move_to_bin(color: str, token: str):
    squares = np.load('backend/assets/squares.npy')
    if squares is None:
        print("Failed to load squares")
        return
    
    robot_centroids = np.array([get_robot_coordinates_of_basket_center(square) for square in squares])
    if color == "light":
        print("Moving to light bin")
        centroid = robot_centroids[0]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
    elif color == "dark":
        print("Moving to dark bin")
        centroid = robot_centroids[1]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token)
        time.sleep(10) 
        open_gripper(token)
    elif color == "unsortable":
        print("Moving to unsortable bin")
        centroid = robot_centroids[2]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
    elif color == "colored":
        print("Moving to colored bin")
        centroid = robot_centroids[3]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)

def pick_up_cloth_and_move_to_bin(token: str, color: str):
    pick_up_cloth(token)
    move_to_bin(color, token)