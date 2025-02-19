import tkinter as tk
from tkinter import filedialog, Scale
from PIL import Image, ImageTk
import cv2
import numpy as np
from edge_detection import detect_edges
from path_generator import PathGenerator
from mouse_drawer import MouseDrawer

class EdgeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edge Detection App")
        
        # Variables
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.path_generator = PathGenerator()
        self.mouse_drawer = MouseDrawer()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # Load image button
        load_btn = tk.Button(btn_frame, text="Load Image", command=self.load_image)
        load_btn.pack(padx=5)
        
        # Threshold slider frame
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(pady=5)
        
        # Threshold spread slider
        tk.Label(slider_frame, text="Edge Sensitivity:").pack()
        self.threshold_spread = Scale(
            slider_frame, 
            from_=0, 
            to=127, 
            orient=tk.HORIZONTAL,
            command=self.on_threshold_change
        )
        self.threshold_spread.set(64)  # Default value
        self.threshold_spread.pack()
        
        # Image display frame
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10)
        
        # Labels for images
        self.original_label = tk.Label(self.image_frame)
        self.original_label.pack(side=tk.LEFT, padx=5)
        
        self.processed_label = tk.Label(self.image_frame)
        self.processed_label.pack(side=tk.LEFT, padx=5)
        
        # Add path parameters frame
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=5)
        
        # Epsilon slider for path simplification
        tk.Label(path_frame, text="Path Simplification:").pack()
        self.epsilon_slider = Scale(
            path_frame,
            from_=0.5,
            to=5.0,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            command=self.on_parameter_change
        )
        self.epsilon_slider.set(2.0)
        self.epsilon_slider.pack()
        
        # Minimum contour length slider
        tk.Label(path_frame, text="Minimum Path Length:").pack()
        self.min_length_slider = Scale(
            path_frame,
            from_=10,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.on_parameter_change
        )
        self.min_length_slider.set(30)
        self.min_length_slider.pack()
        
        # Add another label for path visualization
        self.path_label = tk.Label(self.image_frame)
        self.path_label.pack(side=tk.LEFT, padx=5)
        
        # Draw button
        draw_btn = tk.Button(btn_frame, text="Draw in Paint", command=self.draw_in_paint)
        draw_btn.pack(padx=5)
        
    def load_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if self.image_path:
            # Load and display original image
            image = Image.open(self.image_path)
            image = image.resize((400, 400))  # Resize for display
            self.original_image = ImageTk.PhotoImage(image)
            self.original_label.configure(image=self.original_image)
            self.original_label.image = self.original_image
            # Process image immediately after loading
            self.process_image()
            
    def on_threshold_change(self, value):
        if self.image_path:
            self.process_image()
            
    def process_image(self):
        if self.image_path:
            # Get threshold spread value
            spread = self.threshold_spread.get()
            
            # Perform edge detection
            edges = detect_edges(self.image_path, spread)
            
            # Update path generator parameters
            self.path_generator.epsilon = self.epsilon_slider.get()
            self.path_generator.min_contour_length = self.min_length_slider.get()
            
            # Generate and visualize paths
            paths = self.path_generator.generate_paths(edges)
            path_visualization = self.path_generator.visualize_paths(
                edges.shape, paths
            )
            
            # Display edge detection result
            edge_image = Image.fromarray(edges)
            edge_image = edge_image.resize((400, 400))
            self.processed_image = ImageTk.PhotoImage(edge_image)
            self.processed_label.configure(image=self.processed_image)
            self.processed_label.image = self.processed_image
            
            # Display path visualization
            path_image = Image.fromarray(path_visualization)
            path_image = path_image.resize((400, 400))
            self.path_visualization = ImageTk.PhotoImage(path_image)
            self.path_label.configure(image=self.path_visualization)
            self.path_label.image = self.path_visualization
    
    def on_parameter_change(self, value):
        self.process_image()

    def draw_in_paint(self):
        if hasattr(self, 'path_generator') and self.image_path:
            # Get current paths
            edges = detect_edges(self.image_path, self.threshold_spread.get())
            paths = self.path_generator.generate_paths(edges)
            
            # Get drawing area from user
            drawing_area = self.mouse_drawer.get_drawing_position()
            
            # Draw the paths
            self.mouse_drawer.draw_paths(paths, drawing_area, scale=1.0)

def main():
    root = tk.Tk()
    app = EdgeDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
