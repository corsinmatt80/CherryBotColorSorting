import cv2
from src.utils.color_ranges import COLOR_RANGES
from src.robot_control.robot_control_http import move, toggle

def sorting_mechanism(current_clothing : tuple[int,int,int]) -> str:
    for color_name, color_ranges in COLOR_RANGES.items():
        for color_range in color_ranges:
            color_range_low, color_range_high = color_range
            if check_if_between(current_clothing, color_range_low, color_range_high):
                return color_name
    return ""



def check_if_between(current_clothing : tuple[int, int, int],
                     color_range_low : tuple[int, int, int],
                     color_range_high : tuple [int, int, int]) -> bool:
    #others are fixed (int, int, int)
    if len(current_clothing) != 3:
        return False
    zipped_tuples = zip(color_range_low, current_clothing, color_range_high)

    for color_low, current_clothing_color, color_high in zipped_tuples:
        if not color_low <= current_clothing_color <= color_high:
            return False

    return True

def sort_clothes_by_color(token, contours, colors, color_ranges):
    
    for contour, hsv_color in zip(contours, colors):
        # Get the bin coordinates and orientation for the detected color
        bin_location = color_ranges.get_bin_location(hsv_color)
        
        
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            arm_x, arm_y, arm_z = image_to_arm_coordinates(cx, cy)
        
            # Move the robot arm to pick the cloth
            move(arm_x, arm_y, arm_z - 50, 0, 180, 0, token)  # Adjust Z for picking height

            # Open the gripper to pick the cloth
            open_gripper(token)
            
            # Move to the designated bin to drop the cloth
            new_x, new_y, new_z, new_pitch, new_roll, new_yaw = bin_location
            move(new_x, new_y, new_z, new_pitch, new_roll, new_yaw, token)
            # Close gripper to release the cloth
            close_gripper(token)
            # Optional: Move the arm to a safe position after dropping off the cloth


# These functions are placeholders for the actual implementation

def image_to_arm_coordinates(cx, cy):
    # Placeholder for conversion logic
    # This should convert image pixel coordinates to real-world coordinates
    scaling_factor_x = 1.0
    scaling_factor_y = 1.0
    default_z = 200  # Default height for picking
    return (cx * scaling_factor_x, cy * scaling_factor_y, default_z)

def open_gripper(token):
    toggle(token, 40)
    print("Gripper opened")

def close_gripper(token):
    toggle(token, 0)
    print("Gripper closed")