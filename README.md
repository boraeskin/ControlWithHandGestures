# Hand Gesture Volume and Brightness Control
![Image](https://github.com/user-attachments/assets/896bfd05-d290-4a61-8d54-656a94980ae6)
## Description

The **Hand Gesture Volume and Brightness Control** is a **Computer Vision** project that uses **OpenCV** and **Mediapipe** to control system volume and screen brightness using hand gestures. The program detects hand landmarks and uses the distance between the thumb and index finger to adjust volume (left hand) and brightness (right hand). It also includes a feature to exit the program by bringing both thumbs close together.

**Note**: This project is **only compatible with Windows OS** due to its reliance on the `pycaw` library for volume control and the `screen-brightness-control` library for brightness adjustment.

---

## Features
- **Volume Control**:
  - Use your **left hand** to control system volume.
  - The distance between the thumb and index finger is mapped to the volume level.

- **Brightness Control**:
  - Use your **right hand** to control screen brightness.
  - The distance between the thumb and index finger is mapped to the brightness level.

- **Exit Gesture**:
  - Bring both thumbs close together (less than 30 pixels apart) to exit the program.

- **Visual Feedback**:
  - Real-time visualization of hand landmarks (circles and lines).
  - Display of volume and brightness levels as text.
  - Vertical bars for volume (red) and brightness (yellow).

---

## How to Use the Project

### Prerequisites
Before running the project, ensure you have the following installed:
- Python (3.7 or later)
- OpenCV (`opencv-python`)
- Mediapipe (`mediapipe`)
- Pycaw (`pycaw`)
- Screen Brightness Control (`screen-brightness-control`)
- Comtypes (`comtypes`)

You can install these libraries using `pip`:

   ``bash
pip install opencv-python mediapipe pycaw screen-brightness-control comtypes


### Setting Up the Project

1. **Clone or Download the Project**:
   - Clone this repository or download it as a ZIP file.

   ``bash
   git clone that i will enter later 

2. **Run the Script:**:

3. **Use The Program:**:
- Left Hand: Adjust volume by moving your thumb and index finger closer or farther apart.
- Right Hand: Adjust brightness by moving your thumb and index finger closer or farther apart.
- Exit: Bring both thumbs close together to exit the program.


## Project Structure
ControlWithHandGestures/
├── controlWithHandGestures.py     # Main script for hand gesture detection and control
├── README.md                      # Project documentation


## Technologies Used
- OpenCV: For camera input and image processing.
- Mediapipe: For hand tracking and landmark detection
- Pycaw: For system volume control (Windows-only).
- Screen Brightness Control: For screen brightness adjustment.
- Comtypes: For interfacing with Windows Core Audio API.

## Author
- Bora Eskin
- https://github.com/boraeskin
- bora030303@hotmail.com
