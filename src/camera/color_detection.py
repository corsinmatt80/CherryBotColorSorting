import cv2


def save_image():
    camera_url = ("https://interactions.ics.unisg.ch/61-102/cam5/live-stream")
    cap = cv2.VideoCapture(camera_url)

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera Frame", frame)
            cv2.imwrite("../assets/cloth.jpg", frame)
            cv2.waitKey(1)
            cv2.destroyAllWindows()
        else:
            print("Failed to capture")
    else:
        print("Failed to connect")
    cap.release()


def get_color_in_middle() -> tuple[int, int, int]:
    save_image()

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


get_color_in_middle()
