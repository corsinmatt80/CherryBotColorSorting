from flask import Flask, render_template, request, jsonify
from backend.camera.camera_stream import capture_process_image, are_images_equal, save_image
from backend.camera.color_detection import get_average_color, can_be_sorted, classify_clothes
from backend.robot_control.sort_clothes import pick_up_cloth_and_move_to_bin
from backend.robot_control.robot_control_http import get_token
from backend.basket_detection.detect_basket import detect_baskets
import cv2
import threading
import time

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
sorting_status = {"running": False, "message": "", "logs": []}

class LaundrySorter:
    def __init__(self, base_image_name: str, email: str, name: str):
        self.email = email
        self.name = name
        self.base_image_path = "assets/" + base_image_name
        self.token = get_token()

    def run(self):
        global sorting_status
        sorting_status["running"] = True
        sorting_status["message"] = "Sorting process started."
        sorting_status["logs"].append("Sorting process started.")

        while sorting_status["running"]:
            capture_process_image("assets/cloth")
            current_image_path = "assets/cloth_cropped.jpg"
            current_image = cv2.imread(current_image_path)
            if current_image is None:
                continue

            if are_images_equal(self.base_image_path, current_image_path):
                sorting_status["message"] = "Sorting process is complete."
                sorting_status["logs"].append("Sorting process is complete.")
                break
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
                    break

        sorting_status["running"] = False

@app.route("/")
def index():
    return render_template("index.html")

# Route to display the basket setup page
@app.route("/setup_baskets", methods=["GET", "POST"])
def setup_baskets():
    if request.method == "POST":
        # Handle user input (accept or drag to adjust)
        action = request.json.get("action")
        if action == "accept":
            # User accepted the baskets
            return jsonify({"status": "Baskets accepted"})
        elif action == "adjust":
            # User wants to adjust baskets; handle the adjustment logic
            new_basket_positions = request.json.get("baskets")
            # Save new basket positions here (implement logic to save)
            return jsonify({"status": "Baskets adjusted", "positions": new_basket_positions})

    # On GET, display the processed image
    processed_image_path, squares = detect_baskets()
    return render_template("setup_baskets.html", image_path=processed_image_path, squares=squares)

@app.route("/start_sorting", methods=["POST"])
def start_sorting():
    global sorting_status
    if not sorting_status["running"]:
        sorter = LaundrySorter(base_image_name="cloth", email="yippie.mail@gmail.com", name="yeetmaster")
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
