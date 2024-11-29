import cv2
import numpy as np
from src.camera.camera_stream import save_image


def get_color_in_middle() -> tuple[int, int, int]:
    save_image("cloth")

    cloth = cv2.imread("../assets/cloth.jpg")
    if cloth is None:
        print("Failed to load image")
    else:
        height, width, _ = cloth.shape
        center_y = height / 2
        center_x = width / 2
        (b, g, r) = cloth[int(center_y), int(center_x)]
        rgb = (int(r), int(g), int(b))
        return rgb
    return None

def get_average_color(image_path) -> tuple[int, int, int]:
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image")
        return None

    # Calculate the average color of each channel
    average_color_per_row = np.average(image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = tuple([int(c) for c in average_color[::-1]])  # Convert BGR to RGB and make integers
    return average_color

def classify_clothes(average_color: tuple) -> str:
        r, g, b = average_color
        brightness = np.sqrt(0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2)
        
        if brightness > 200:
            return "light"
        elif brightness < 50:
            return "dark"
        elif max(r, g, b) > 100 and abs(r - g) < 20 and abs(g - b) < 20 and abs(b - r) < 20:
            return "unsortable"
        else:
            return "colored"

# if the amount of black is similar to the amount of white in a cloth, the cloth cannot be sorted.
def can_be_sorted(image_path: str, white_threshold: int = 230, black_threshold: int = 25, tolerance: float = 5.0) -> bool:
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Failed to load image")
        return False

    # Count the number of white and black pixels
    white_pixels = np.sum(image >= white_threshold)
    black_pixels = np.sum(image <= black_threshold)
    total_pixels = image.size

    white_percentage = (white_pixels / total_pixels) * 100
    black_percentage = (black_pixels / total_pixels) * 100

    # Check if the percentages are within the tolerance range
    return abs(white_percentage - black_percentage) > tolerance

def configure_camera():
    return get_color_in_middle()