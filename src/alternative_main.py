from src.camera.image_processor import ImageProcessor
from src.utils.color_ranges import ColorRanges
from src.robot_control.sorting_mechanism import sort_clothes_by_color


def alternative_main():
    processor = ImageProcessor(background_color_threshold = ((0, 0, 200), (180, 30, 255)))  # white background, change as needed
    contours, colors = processor.process_image()
    colors_ranges = ColorRanges()
    sort_clothes_by_color(token="token", contours=contours, colors=colors, color_ranges=colors_ranges)