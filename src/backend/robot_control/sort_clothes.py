from backend.robot_control.robot_control_http import move, toggle, open_gripper, close_gripper
import numpy as np
from backend.utils.image_to_robot import get_robot_coordinates_of_basket_center
import time

# Initialize counters for each bin
light_bin_count = 0
dark_bin_count = 0
unsortable_bin_count = 0
colored_bin_count = 0

def pick_up_cloth(token: str):
    open_gripper(token)
    time.sleep(1)
    move(450, 0, 15, -180, 0, -180, token) # Use coordinates of the cloth pile
    time.sleep(11)
    close_gripper(token)
    time.sleep(5)

def move_to_bin(color: str, token: str):
    global light_bin_count, dark_bin_count, unsortable_bin_count, colored_bin_count
    
    squares = np.load('backend/assets/squares.npy')
    if squares is None:
        print("Failed to load squares")
        return
    
    robot_centroids = np.array([get_robot_coordinates_of_basket_center(square) for square in squares])
    if color == "light":
        print("Moving to light bin")
        centroid = robot_centroids[0]
        move(float(centroid[0]), float(centroid[1]), 100, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
        light_bin_count += 1
        if light_bin_count == 10:
            print("Light bin is full")
    elif color == "dark":
        print("Moving to dark bin")
        centroid = robot_centroids[1]
        move(float(centroid[0]), float(centroid[1]), 100, -180, 0, -180, token)
        time.sleep(10) 
        open_gripper(token)
        dark_bin_count += 1
        if dark_bin_count == 10:
            print("Dark bin is full")
    elif color == "unsortable":
        print("Moving to unsortable bin")
        centroid = robot_centroids[2]
        move(float(centroid[0]), float(centroid[1]), 100, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
        unsortable_bin_count += 1
        if unsortable_bin_count == 10:
            print("Unsortable bin is full")
    elif color == "colored":
        print("Moving to colored bin")
        centroid = robot_centroids[3]
        move(float(centroid[0]), float(centroid[1]), 100, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
        colored_bin_count += 1
        if colored_bin_count == 10:
            print("Colored bin is full")

def pick_up_cloth_and_move_to_bin(token: str, color: str):
    pick_up_cloth(token)
    move_to_bin(color, token)

# Create an API endpoint to get the bin counts
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/bin_counts', methods=['GET'])
def get_bin_counts():
    return jsonify({
        'light_bin_count': light_bin_count,
        'dark_bin_count': dark_bin_count,
        'unsortable_bin_count': unsortable_bin_count,
        'colored_bin_count': colored_bin_count
    })

if __name__ == '__main__':
    app.run(debug=True)