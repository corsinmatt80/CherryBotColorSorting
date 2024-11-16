from camera.color_detection import *
import keyboard
import time
from src.robot_control.motion_controller import move_to_bin
from src.robot_control.sorting_mechanism import sorting_mechanism


def main():
    rgb_configuration = configure_camera()
    while not keyboard.is_pressed('enter'):
        time.sleep(1000)

    print("Starting Cloth-Sorting by Color")

    if not tuple_difference(get_color_in_middle(), rgb_configuration):
        print("Please lay your clothes on the table!")
        while not tuple_difference(get_color_in_middle(), rgb_configuration):
            time.sleep(1000)


    print("Starting")

    while tuple_difference(get_color_in_middle(), rgb_configuration):
        color = sorting_mechanism(get_color_in_middle())
        if color == "":
            print("Color wasn't recognized!")
        else:
            move_to_bin(color)


def tuple_difference(tuple1, tuple2, tolerance = 5) -> bool:
    if len(tuple1) != len(tuple2):
        return False
    zipped_tuples = zip(tuple1, tuple2)

    for value1, value2 in zipped_tuples:
        if not value1-value2 <= tolerance:
            return False

    return True





if __name__ == '__main__':
    main()



