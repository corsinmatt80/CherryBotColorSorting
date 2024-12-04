from backend.robot_control.robot_control_http import move, toggle
import numpy as np
from backend.utils.image_to_robot import get_robot_coordinates_of_basket_center

def pick_up_cloth(token: str):
    move(475, 0, 0, -180, 0, -180, token) # Use coordinates of the cloth pile
    toggle(token)

def move_to_bin(color: str, token: str):
    squares = np.load('assets/squares.npy')
    if squares is None:
        print("Failed to load squares")
        return
    
    robot_centroids = np.array([get_robot_coordinates_of_basket_center(square) for square in squares])
    if color == "light":
        centroid = robot_centroids[0]
        move(centroid[0], centroid[1], 100, -180, 0, -180, token) 
        toggle(token)
    elif color == "dark":
        centroid = robot_centroids[1]
        move(centroid[0], centroid[1], 100, -180, 0, -180, token) 
        toggle(token)
    elif color == "unsortable":
        centroid = robot_centroids[2]
        move(centroid[0], centroid[1], 100, -180, 0, -180, token) 
        toggle(token)
    elif color == "colored":
        centroid = robot_centroids[3]
        move(centroid[0], centroid[1], 100, -180, 0, -180, token) 
        toggle(token)

def pick_up_cloth_and_move_to_bin(token: str, color: str):
    pick_up_cloth(token)
    move_to_bin(color, token)