import cv2
import numpy as np
from backend.camera.camera_stream import save_image


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
        
def classify_color(average_color):
    r, g, b = average_color
    brightness = np.sqrt(0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2)
    
    if brightness > 200:
        return "light"
    elif brightness < 50:
        return "dark"
    else:
        return "colored"

def classify_clothes(image_path):
    # Step 1: Read the image
    img = cv2.imread(image_path)
    
    # Step 2: Convert the image to HSV color space
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Step 3: Extract the Value (brightness) and Saturation channels
    h, s, v = cv2.split(hsv_img)
    
    # Step 4: Calculate average saturation and brightness
    avg_saturation = np.mean(s)
    avg_brightness = np.mean(v)
    
    # Step 5: Classify light/dark based on average brightness (V channel)
    if avg_brightness < 85:  # Dark image threshold (0-255 scale)
        brightness_category = "dark"
    else:
        brightness_category = "light"
    
    # Step 6: Classify colorful/gray based on average saturation (S channel)
    if avg_saturation < 50:  # Low saturation means grayscale-like
        color_category = "grayscale"
    else:
        color_category = "colorful"
    
    # Step 7: Classify as light, dark, or colorful
    if brightness_category == "light" and color_category == "grayscale":
        return "light"
    elif brightness_category == "dark" and color_category == "grayscale":
        return "dark"
    elif color_category == "colorful":
        return "colored"
    else:
        return "unsortable"  # In case the image is too uniform or ambiguous

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