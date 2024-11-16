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