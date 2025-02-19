import numpy as np
import cv2
# import pyautogui
import time

class PathGenerator:
    def __init__(self):
        self.epsilon = 2.0  # Default path simplification factor
        self.min_contour_length = 30  # Minimum length for a contour to be considered
        
    def generate_paths(self, edge_image):
        """
        Generate paths from edge detected image
        
        Args:
            edge_image (numpy.ndarray): Binary edge image from Canny detection
            
        Returns:
            list: List of contours (paths) as numpy arrays
        """
        # Find contours in the edge image
        contours, _ = cv2.findContours(
            edge_image, 
            cv2.RETR_LIST, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter and simplify contours
        simplified_contours = []
        for contour in contours:
            # Skip if contour is too short
            if len(contour) < self.min_contour_length:
                continue
                
            # Simplify the contour using Douglas-Peucker algorithm
            epsilon = self.epsilon
            simplified = cv2.approxPolyDP(contour, epsilon, closed=False)
            simplified_contours.append(simplified)
            
        return simplified_contours
    
    def visualize_paths(self, image_shape, paths):
        """
        Create a visualization of the paths
        
        Args:
            image_shape (tuple): Shape of the original image (height, width)
            paths (list): List of contours to visualize
            
        Returns:
            numpy.ndarray: Image with drawn paths
        """
        # Create blank image
        visualization = np.zeros(image_shape, dtype=np.uint8)
        
        # Draw all paths
        cv2.drawContours(visualization, paths, -1, (255, 255, 255), 1)
        
        return visualization
