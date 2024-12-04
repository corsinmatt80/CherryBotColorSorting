import cv2

def save_image(path : str):
    camera_url = ("https://interactions.ics.unisg.ch/61-102/cam5/live-stream")
    cap = cv2.VideoCapture(camera_url)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(path+".jpg", frame)
            cv2.destroyAllWindows()
        else:
            print("Failed to capture")
    else:
        print("Failed to connect")
    cap.release()

# x,y are the coordinates of the top left corner
def crop_image(path: str, path_crop: str):
    image = cv2.imread(path + ".jpg")
    if image is None:
        print("Failed to load image")
        return

    # Cropping the image
    crop_img = image[180:230, 260:330]

    # Save the cropped image
    cv2.imwrite(path_crop +".jpg", crop_img)

def capture_process_image(path : str):
    save_image(path)
    crop_image(path, path + "_cropped")

def are_images_equal(image_path1: str, image_path2: str) -> bool:
    # Load the two images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    if image1 is None or image2 is None:
        print("One or both images failed to load.")
        return False

    # Check if the images are the same size and type
    if image1.shape != image2.shape:
        print("Images have different sizes or color channels.")
        return False

    # Check if the images have the same content
    difference = cv2.absdiff(image1, image2)
    b, g, r = cv2.split(difference)

    # Check how many pixels have a difference greater than 10
    if difference.sum() > 100000:
        print(f"Difference: {difference.sum()}")
        print(b.sum(), g.sum(), r.sum())
        return False
    else:
        print("No clothes detected.")
        return True
        

