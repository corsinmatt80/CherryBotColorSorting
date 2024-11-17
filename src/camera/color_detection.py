import cv2
from camera_stream import save_image


def get_color_in_middle() -> tuple[int, int, int]:
    save_image("cloth.jpg")

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


def configure_camera():
    return get_color_in_middle()