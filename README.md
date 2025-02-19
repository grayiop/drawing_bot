# Drawing Bot

A Python application that converts images into line drawings and automatically draws them using mouse control. This tool uses computer vision techniques to detect edges in images and recreates them as drawings in any paint program.

## Features

- Edge detection with adjustable sensitivity
- Path simplification controls
- Real-time preview of edge detection and drawing paths
- Interactive drawing area selection
- Automatic drawing using mouse control
- Support for various image formats (JPG, PNG, BMP, GIF, TIFF)

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Tkinter
- Pillow (PIL)
- PyAutoGUI
- keyboard
- mouse

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/drawing_bot.git
cd drawing_bot
```
2. Install required packages:
TODO
## Usage

1. Run the application:
```bash
python ui.py
```
2. Use the interface to:
   - Load an image using the "Load Image" button
   - Adjust edge detection sensitivity using the slider
   - Fine-tune path simplification and minimum path length
   - Click "Draw in Paint" when ready

3. When drawing:
   - Open your preferred drawing program (e.g., Paint)
   - Click to select the top-left corner of your drawing area
   - Click to select the bottom-right corner
   - The bot will automatically start drawing after a 3-second delay
   - Press ESC at any time to stop the drawing process

## How It Works

1. **Edge Detection**: Uses the Canny edge detection algorithm to identify edges in the input image
2. **Path Generation**: Converts edges into drawable paths using contour detection
3. **Path Simplification**: Applies the Douglas-Peucker algorithm to simplify paths for smoother drawing
4. **Automated Drawing**: Controls the mouse to draw the generated paths in your preferred drawing program

## Safety Note

This application uses PyAutoGUI for mouse control. A failsafe is implemented - quickly move your mouse to any screen corner to abort the drawing process.

## License

TODO

## Contributing

Feel free to open issues or submit pull requests to help improve this project.
