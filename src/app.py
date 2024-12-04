from flask import Flask, render_template, request, jsonify
from backend.camera.camera_stream import capture_process_image, are_images_equal, save_image
from backend.camera.color_detection import get_average_color, can_be_sorted, classify_clothes
from backend.robot_control.sort_clothes import pick_up_cloth_and_move_to_bin
from backend.robot_control.robot_control_http import log_on, get_token
from backend.basket_detection.detect_basket import detect_baskets
import cv2
import threading
import time
import numpy as np
import os

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
sorting_status = {"running": False, "message": "", "logs": []}



class LaundrySorter:
    def __init__(self, base_image_name: str, email: str, name: str):
        self.email = email
        self.name = name
        self.base_image_path = base_image_name + "_cropped.jpg"
        self.token = log_on(email, name)

    def run(self):
        global sorting_status
        sorting_status["running"] = True
        sorting_status["message"] = "Sorting process started."
        sorting_status["logs"].append("Sorting process started.")

        while sorting_status["running"]:
            capture_process_image("cloth")
            current_image_path = "cloth_cropped.jpg"
            current_image = cv2.imread(current_image_path)
            if current_image is None:
                continue

            if are_images_equal(self.base_image_path, current_image_path):
                sorting_status["message"] = "Sorting process is complete."
                sorting_status["logs"].append("Sorting process is complete.")
            else:
                sorting_status["message"] = "Clothing detected on the table."
                sorting_status["logs"].append("Clothing detected on the table.")
                if can_be_sorted(current_image_path):
                    avg_color = get_average_color(current_image_path)
                    sorting_status["logs"].append(f"Image can be sorted. Average color: {avg_color}")
                    cloth_type = classify_clothes(avg_color)
                    pick_up_cloth_and_move_to_bin(token=self.token, color=cloth_type)
                else:
                    sorting_status["logs"].append("Image cannot be sorted automatically, please sort manually.")
                    pick_up_cloth_and_move_to_bin(token=self.token, color="unsortable")
            time.sleep(1)

        sorting_status["running"] = False



@app.route("/")
def index():
    return render_template("index.html")

# Route to display the basket setup page
@app.route("/setup_baskets", methods=["POST"])
def setup_baskets():
    # Check if the response contains four squares
    squares = request.json.get("squares")
    if len(squares) != 4:
        return jsonify({"status": "Invalid number of squares"})
    else:
        # Save squares in /Backend/assets
        save_directory = os.path.join("backend", "assets")
        os.makedirs(save_directory, exist_ok=True)
        save_path = os.path.join(save_directory, "squares.npy")
        np.save(save_path, squares)
        print("Squares received:", squares)
        return jsonify({"status": "Squares received"})


@app.route("/setup_baskets", methods=["GET"])
def get_basket_setup():
    # On GET, display the processed image
    processed_image_path, squares = detect_baskets()
    squares_serializable = [square.tolist() for square in squares]
    return render_template("setup_baskets.html", image_path=processed_image_path, squares=squares_serializable)

# Check if the baskets are set up
@app.route("/check_baskets", methods=["GET"])
def check_baskets():
    save_path = os.path.join("backend", "assets", "squares.npy")
    if os.path.exists(save_path):
        return jsonify({"status": "Baskets set up"})
    else:
        return jsonify({"status": "Baskets not set up"})


@app.route("/start_sorting", methods=["POST"])
def start_sorting():
    global sorting_status
    if not sorting_status["running"]:
        base_image_name="base_image"
        capture_process_image("base_image")
        sorter = LaundrySorter(base_image_name, email="yippie.mail@gmail.com", name="yeetmaster")
        thread = threading.Thread(target=sorter.run)
        thread.start()
        return jsonify({"status": "Sorting started"})
    else:
        return jsonify({"status": "Sorting already in progress"})

@app.route("/status", methods=["GET"])
def status():
    global sorting_status
    return jsonify(sorting_status)

if __name__ == "__main__":
    app.run(debug=True)
