import cv2
import numpy as np

# Corresponding points in image coordinates and robot coordinates
image_points = np.array([[281, 169], [397, 326], [181, 299]], dtype=np.float32)
robot_points = np.array([[399, -1.15116775e-14], [600, 200], [600, -200]], dtype=np.float32)

# Calculate the affine transformation matrix
M = cv2.getAffineTransform(image_points, robot_points)

# Now you can use this matrix to transform any point from the image to robot coordinates
def transform_point(x, y):
    # Apply the affine transformation
    point = np.array([[x, y]], dtype=np.float32)
    transformed_point = cv2.transform(point[None, :, :], M)  # Apply transformation
    return transformed_point[0][0]  # Extract the transformed point

def calculate_centroid(corners):
    x_coords = corners[:, 0]
    y_coords = corners[:, 1]
    centroid_x = np.mean(x_coords)
    centroid_y = np.mean(y_coords)
    return centroid_x, centroid_y

def get_robot_coordinates_of_basket_center(corners):
    centroid_x, centroid_y = calculate_centroid(corners)
    robot_coords = transform_point(centroid_x, centroid_y)
    return robot_coords


