import cv2
from src.camera.camera_stream import save_image, capture_process_image, are_images_equal
from src.camera.color_detection import get_average_color, can_be_sorted, classify_clothes
from src.robot_control.sort_clothes import pick_up_cloth_and_move_to_bin

class LaundrySorter:
    def __init__(self, base_image_name: str):
        self.base_image_path = "../assets/" + base_image_name
        self.base_image = cv2.imread(self.base_image_path)
        if self.base_image is None:
            print("Failed to load base image.")
            raise IOError("Base image could not be loaded.")
        
    def run(self):
        while True:
            current_image = capture_process_image("cloth")
            if current_image is None:
                continue
            
            if are_images_equal(self.base_image, current_image):
                print("Image is identical to the base image. No clothing detected.")
            else:
                # Image has changed, meaning clothing has been detected
                print("Clothing detected on the table.")
                if can_be_sorted(current_image):
                    avg_color = get_average_color(current_image)
                    print(f"Image can be sorted. Average color: {avg_color}")
                    cloth_type = classify_clothes(avg_color)
                    pick_up_cloth_and_move_to_bin(token = "define", color = cloth_type)
                else:
                    print("Image cannot be sorted automatically, please sort manually.")
                break  # Stop after detecting different image

   

# Example usage
if __name__ == "__main__":
    sorter = LaundrySorter("base.jpg")
    sorter.run()
