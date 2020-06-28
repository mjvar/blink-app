# Blink Detection

This folder contains all code necessary to detect user eye movements with OpenCV. It was largely adapted from Adrian Roseberg's [blog post](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/) on blink detection with OpenCV.

## Getting Started

### Prerequisites

This project requires the following tools:
- NumPy: Python library adding support for mathematical functions
- SciPy: Python library adding support for technical computing
- imutils: Convenience functions to make basic image processing functions easier in OpenCV and Python
- threading: Python library providing high-level support for multithreaded programming
- requests: HTTP library to make requests in Python easier
- argparse: Parser for command line options and arguments
- time: Module to help track time
- dlib: Toolkit for making real world machine learning and data analysis applications
- OpenCV: Library of functions aimed at real-time computer vision

### Testing

Run the file with the below command line argument:

`python3 blink_detect.py --shape-predictor shape_predictor_68_face_landmarks.dat --webcam 1`

