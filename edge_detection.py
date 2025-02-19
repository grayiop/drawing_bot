import cv2
import numpy as np

def detect_edges(image_path, threshold_spread=127):
    """
    Perform edge detection on the input image using Canny algorithm
    
    Args:
        image_path (str): Path to the input image
        threshold_spread (int): Value determining the spread between low and high thresholds.
                              Higher spread means more contrast in edge detection.
                              Low threshold = 127 - spread
                              High threshold = 127 + spread
        
    Returns:
        numpy.ndarray: Edge detected image
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Calculate thresholds based on spread
    low_threshold = max(0, 127 - threshold_spread)
    high_threshold = min(255, 127 + threshold_spread)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, low_threshold, high_threshold)
    
    return edges
