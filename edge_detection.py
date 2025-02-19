import cv2
import numpy as np

def detect_edges(image_path, threshold_spread=127):
    """
    Perform enhanced edge detection on the input image
    
    Args:
        image_path (str): Path to the input image
        threshold_spread (int): Value determining the spread between low and high thresholds.
                              Higher spread means more contrast in edge detection.
                              
    Returns:
        numpy.ndarray: Edge detected image
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter instead of Gaussian blur
    # This preserves edges better while still reducing noise
    blurred = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)
    
    # Calculate thresholds based on spread
    low_threshold = max(0, 127 - threshold_spread)
    high_threshold = min(255, 127 + threshold_spread)
    
    # Apply Canny edge detection
    edges_canny = cv2.Canny(blurred, low_threshold, high_threshold)
    
    # Additional edge detection using Sobel
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalize Sobel output
    sobel = np.uint8(255 * sobel / np.max(sobel))
    
    # Threshold Sobel edges
    _, sobel_thresh = cv2.threshold(sobel, low_threshold, 255, cv2.THRESH_BINARY)
    
    # Combine Canny and Sobel edges
    edges = cv2.bitwise_or(edges_canny, sobel_thresh)
    
    # Optional: Apply slight morphological operations to connect nearby edges
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    return edges
