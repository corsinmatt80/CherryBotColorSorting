from backend.robot_control.robot_control_http import move, toggle, open_gripper, close_gripper
import numpy as np
from backend.utils.image_to_robot import get_robot_coordinates_of_basket_center
import time

class BinCounter:
    def __init__(self):
        self.light_bin_count = 0
        self.dark_bin_count = 0
        self.unsortable_bin_count = 0
        self.colored_bin_count = 0

    def increment(self, bin_type):
        if bin_type == "light":
            self.light_bin_count += 1
            if self.light_bin_count == 10:
                print("Light bin is full")
        elif bin_type == "dark":
            self.dark_bin_count += 1
            if self.dark_bin_count == 10:
                print("Dark bin is full")
        elif bin_type == "unsortable":
            self.unsortable_bin_count += 1
            if self.unsortable_bin_count == 10:
                print("Unsortable bin is full")
        elif bin_type == "colored":
            self.colored_bin_count += 1
            if self.colored_bin_count == 10:
                print("Colored bin is full")

bin_counter = BinCounter()

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
    global light_bin_count, dark_bin_count, unsortable_bin_count, colored_bin_count
    
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
        bin_counter.increment("light")
    elif color == "dark":
        print("Moving to dark bin")
        centroid = robot_centroids[1]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token)
        time.sleep(10) 
        open_gripper(token)
        bin_counter.increment("dark")
    elif color == "unsortable":
        print("Moving to unsortable bin")
        centroid = robot_centroids[2]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
        bin_counter.increment("unsortable")
    elif color == "colored":
        print("Moving to colored bin")
        centroid = robot_centroids[3]
        move(float(centroid[0]), float(centroid[1]), 200, -180, 0, -180, token) 
        time.sleep(10)
        open_gripper(token)
        bin_counter.increment("colored")

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