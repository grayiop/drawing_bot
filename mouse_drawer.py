import pyautogui
import time
import keyboard
import mouse

class MouseDrawer:
    def __init__(self):
        pyautogui.FAILSAFE = True
        
    def draw_paths(self, paths, drawing_area, scale=1.0, delay=0.13):
        top_left, bottom_right = drawing_area
        canvas_width = bottom_right[0] - top_left[0]
        canvas_height = bottom_right[1] - top_left[1]
        
        # Find the bounding box of all paths
        min_x = min(point[0][0] for path in paths for point in path)
        max_x = max(point[0][0] for path in paths for point in path)
        min_y = min(point[0][1] for path in paths for point in path)
        max_y = max(point[0][1] for path in paths for point in path)
        
        # Calculate original aspect ratio and dimensions
        original_width = max_x - min_x
        original_height = max_y - min_y
        
        # Calculate scaling factors for width and height
        width_scale = canvas_width / original_width
        height_scale = canvas_height / original_height
        
        # Use the smaller scale to maintain aspect ratio
        scale_factor = min(width_scale, height_scale)
        
        # Calculate centered position
        actual_width = original_width * scale_factor
        actual_height = original_height * scale_factor
        x_offset = top_left[0] + (canvas_width - actual_width) / 2
        y_offset = top_left[1] + (canvas_height - actual_height) / 2
        
        print("Get ready to draw... (Press ESC to stop drawing)")
        
        try:
            for path in paths:
                if keyboard.is_pressed('esc'):
                    print("\nDrawing cancelled by user")
                    return
                
                # Scale points relative to the actual path bounds
                start_point = path[0][0]
                x = int(x_offset + ((start_point[0] - min_x) * scale_factor))
                y = int(y_offset + ((start_point[1] - min_y) * scale_factor))
                pyautogui.moveTo(x, y)
                
                # Press and hold left mouse button
                pyautogui.mouseDown(button='left')
                
                try:
                    # Draw the path with minimal delay between points
                    for point in path:
                        if keyboard.is_pressed('esc'):
                            raise KeyboardInterrupt
                        x = int(x_offset + ((point[0][0] - min_x) * scale_factor))
                        y = int(y_offset + ((point[0][1] - min_y) * scale_factor))
                        pyautogui.dragTo(x, y, duration=delay, _pause=False)
                finally:
                    # Always release mouse button
                    pyautogui.mouseUp(button='left')
                    time.sleep(0.05)
                    
        except KeyboardInterrupt:
            pyautogui.mouseUp(button='left')
            print("\nDrawing interrupted")
            
    def get_drawing_position(self):
        print("Click the top-left corner of the drawing area...")
        time.sleep(0.5)  # Small delay to prevent accidental clicks
        
        # Wait for first click
        while True:
            if mouse.is_pressed('left'):
                top_left = pyautogui.position()
                break
        time.sleep(0.1)  # Debounce
        
        print("Now click the bottom-right corner of the drawing area...")
        time.sleep(0.5)
        
        # Wait for second click
        while True:
            if mouse.is_pressed('left'):
                bottom_right = pyautogui.position()
                break
        time.sleep(0.1)  # Debounce
        
        # Calculate drawing area dimensions
        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        
        print(f"Drawing area selected: {width}x{height} pixels")
        print("Drawing will start in 3 seconds...")
        time.sleep(3)
        
        return top_left, bottom_right
