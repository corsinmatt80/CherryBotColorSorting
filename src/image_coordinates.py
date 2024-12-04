import cv2
import numpy as np
from backend.camera.camera_stream import save_image

# Initialize the image
save_image("test")
image = cv2.imread('test.jpg')

def calculate_centroid(corners):
    x_coords = corners[:, 0]
    y_coords = corners[:, 1]
    centroid_x = np.mean(x_coords)
    centroid_y = np.mean(y_coords)
    return centroid_x, centroid_y

# This function will be called when the user clicks on the image
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at coordinates: ({x}, {y})")
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)  # Mark the point with a red circle
        cv2.imshow('Image', image)

# Show the image
cv2.imshow('Image', image)
cv2.setMouseCallback('Image', get_coordinates)

cv2.waitKey(0)
cv2.destroyAllWindows()