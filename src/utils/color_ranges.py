class ColorRanges:
    def __init__(self):
        # Define color ranges in HSV (Hue, Saturation, Value) format
        self.ranges = {
            'lights': [(0, 0, 200), (180, 50, 255)],  # Light colors: higher value range
            'darks': [(0, 0, 0), (180, 255, 50)],     # Dark colors: lower value range
            'colors': [(0, 50, 50), (180, 255, 200)]  # Saturated and vibrant colors
        }
        # Define bin locations for each category
        self.bin_locations = {
            'lights': (100, 150, 200, 0, 180, 0),  # Example coordinates and orientation for the lights bin
            'darks': (200, 150, 200, 0, 180, 0),   # Example coordinates and orientation for the darks bin
            'colors': (300, 150, 200, 0, 180, 0)   # Example coordinates and orientation for the colors bin
        }

    def categorize_color(self, hsv_color):
        """Categorizes a given HSV color into lights, darks, or colors."""
        hue, saturation, value = hsv_color

        # Check if the color is a light color
        if self.is_within_range(hsv_color, self.ranges['lights']):
            return 'lights'
        
        # Check if the color is a dark color
        if self.is_within_range(hsv_color, self.ranges['darks']):
            return 'darks'
        
        # If not light or dark, it is considered a colored item
        return 'colors'

    def is_within_range(self, hsv_color, range):
        """Check if a given color is within a specified HSV range."""
        (low_hue, low_sat, low_val), (high_hue, high_sat, high_val) = range
        hue, sat, val = hsv_color
        return (low_hue <= hue <= high_hue) and (low_sat <= sat <= high_sat) and (low_val <= val <= high_val)

    def get_bin_location(self, hsv_color):
        """Determines the bin location for a cloth based on its color category."""
        category = self.categorize_color(hsv_color)
        return self.bin_locations[category]


COLOR_RANGES = {
    "red" : [
        ([0, 120, 70], [10, 255, 255]), #lower range red
        ([170, 120, 70], [180, 255, 255]) #upper range red
    ],
    "dark" : [
        ([0,0,0], [180,255,50]),
    ],
    "light" : [
        ([0, 0, 200], [180, 50, 255])
    ]
}