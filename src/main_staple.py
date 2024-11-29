import cv2
import time
import os
from src.camera.camera_stream import capture_process_image, are_images_equal, save_image
from src.camera.color_detection import get_average_color, can_be_sorted, classify_clothes
from src.robot_control.sort_clothes import pick_up_cloth_and_move_to_bin
from src.robot_control.robot_control_http import  get_token


class LaundrySorter:
    def __init__(self, base_image_name: str, email : str, name : str):
        self.email = email
        self.name = name
        self.base_image_path = "assets/" + base_image_name
        self.token = get_token()


    def test(self):
        save_image("test")


    def run(self):
        while True:
            capture_process_image("assets/cloth")
            current_image_path = "assets/cloth_cropped.jpg"
            current_image = cv2.imread(current_image_path)
            if current_image is None:
                continue
            
            if are_images_equal(self.base_image_path, current_image_path):
                print("Image is identical to the base image. No clothing detected.")
                break
            else:
                print("Not the same")
                print("Clothing detected on the table.")
                if can_be_sorted(current_image_path):
                    avg_color = get_average_color(current_image_path)
                    print(f"Image can be sorted. Average color: {avg_color}")
                    cloth_type = classify_clothes(avg_color)
                    pick_up_cloth_and_move_to_bin(token = self.token, color = cloth_type)
                else:
                    print("Image cannot be sorted automatically, please sort manually.")
                    break  # Stop after detecting different image



# Example usage
if __name__ == "__main__":
    sorter = LaundrySorter(base_image_name = "cloth", email = "yippie.mail@gmail.com", name = "yeetmaster")
    sorter.run()