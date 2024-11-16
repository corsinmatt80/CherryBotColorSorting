from src.utils.color_ranges import COLOR_RANGES

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