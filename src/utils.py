import numpy as np

def calculate_distance(pt1, pt2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

class MovingAverage:
    """Class to smooth values using moving average."""
    def __init__(self, size=5):
        self.size = size
        self.values = []

    def update(self, val):
        self.values.append(val)
        if len(self.values) > self.size:
            self.values.pop(0)
        return np.mean(self.values, axis=0)

def map_value(value, left_min, left_max, right_min, right_max):
    """Map a value from one range to another."""
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)
