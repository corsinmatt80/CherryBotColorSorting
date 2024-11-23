import cv2
import numpy as np
from camera_stream import save_image

class ImageProcessor:
    def __init__(self, background_color_threshold):
        self.background_color_threshold = background_color_threshold

    def preprocess_image(self, image_path):
        """Load image and convert to appropriate color space."""
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Image not found at the path specified.")
        # Convert image to HSV for better color segmentation
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return hsv_image

    def subtract_background(self, hsv_image):
        """Subtract the high contrast tray background using color thresholding."""
        # Assuming the tray is a very distinct color, we can threshold it
        mask = cv2.inRange(hsv_image, self.background_color_threshold[0], self.background_color_threshold[1])
        # Invert mask to get clothes
        clothes = cv2.bitwise_not(mask)
        return clothes

    def find_clothes(self, clothes_mask):
        """Identify distinct items of clothing in the mask."""
        contours, _ = cv2.findContours(clothes_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def get_color_of_cloth(self, image, contour):
        """Calculate the average color of a cloth piece."""
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], -1, color=(255, 255, 255), thickness=cv2.FILLED)
        mean_color = cv2.mean(image, mask=mask)
        return mean_color[:3]  # Return RGB or HSV color depending on your setup

    def process_image(self):
        """Process an image to find clothes and their colors."""
        save_image("cloth.jpg")
        image_path = "../assets/cloth.jpg"
        hsv_image = self.preprocess_image(image_path)
        clothes_mask = self.subtract_background(hsv_image)
        contours = self.find_clothes(clothes_mask)
        clothes_colors = [self.get_color_of_cloth(hsv_image, contour) for contour in contours]
        return contours, clothes_colors
