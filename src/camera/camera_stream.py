import cv2
import numpy as np

def save_image(name : str):
    camera_url = ("https://interactions.ics.unisg.ch/61-102/cam5/live-stream")
    cap = cv2.VideoCapture(camera_url)

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera Frame", frame)
            cv2.imwrite("../assets/"+name+".jpg", frame)
            cv2.waitKey(1)
            cv2.destroyAllWindows()
        else:
            print("Failed to capture")
    else:
        print("Failed to connect")
    cap.release()

# x,y are the coordinates of the top left corner
def crop_image(original_image_name: str, x: int, y: int, width: int, height: int, cropped_image_name: str):
    image = cv2.imread("../assets/" + original_image_name + ".jpg")
    if image is None:
        print("Failed to load image")
        return

    # Cropping the image
    crop_img = image[y:y+height, x:x+width]

    # Save the cropped image
    cv2.imwrite("../assets/" + cropped_image_name, crop_img)

def capture_process_image(name: str):
    save_image(name)
    crop_image(name, 10, 10, 10, 10, name + "_cropped")

def are_images_equal(image_path1: str, image_path2: str) -> bool:
    # Load the two images
    image1 = cv2.imread("../assets/" + image_path1)
    image2 = cv2.imread("../assets/" + image_path2)

    if image1 is None or image2 is None:
        print("One or both images failed to load.")
        return False

    # Check if the images are the same size and type
    if image1.shape != image2.shape:
        print("Images have different sizes or color channels.")
        return False

    # Check if the images have the same content
    difference = cv2.subtract(image1, image2)
    b, g, r = cv2.split(difference)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True
    else:
        return False