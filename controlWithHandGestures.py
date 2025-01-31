# First import the necessary libraries for the project
import cv2  # For working with camera
import mediapipe as mp  # For hand tracking
import math  # For distance calculations
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # For controlling the system volume
import screen_brightness_control as sbc

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 = default camera

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands  # Imports the Hands module from the MediaPipe library.
hands = mp_hands.Hands()  # Create a hands object
mp_draw = mp.solutions.drawing_utils  # For drawing hand landmarks

# Initialize pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # Windows Core Audio API interface
volume = cast(interface, POINTER(IAudioEndpointVolume))  # Cast it to the specific type IAudioEndpointVolume.
volume_range = volume.GetVolumeRange()  # Get the volume range (usually -65.25 to 0.0)
min_volume = volume_range[0]  # for min volume
max_volume = volume_range[1]  # for max volume

# Defining Distance Functions

# Function to calculate 3D distance between two points (for volume and brightness control)
def calculate_3d_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)  # 3D Euclidean distance

# Function to calculate 2D distance between two points (for quitting with thumb touches)
def calculate_2d_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # 2D Euclidean distance

# Dictionary to store thumb positions
hand_landmarks = {}

while True:
    success, img = cap.read()
    if not success:
        break  # Handling Camera or Video Errors

    img = cv2.flip(img, 1)  # Flip the cam for a mirror effect

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert the image BGR to RGB (MediaPipe requires it)
    results = hands.process(img_rgb)

    # If hands are detected
    if results.multi_hand_landmarks:
        hand_landmarks.clear()  # Reset stored landmarks

        for hand_landmarks_obj, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(img, hand_landmarks_obj, mp_hands.HAND_CONNECTIONS)  # Draw landmarks on the image

            thumb_tip = hand_landmarks_obj.landmark[4]  # Thumb tip (landmark 4)
            index_tip = hand_landmarks_obj.landmark[8]  # Index finger tip (landmark 8)

            # Convert landmark positions to pixel coordinates
            h, w, c = img.shape  # height, width, number of color channels (3 for RGB)
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Draw circles at the thumb and index finger tips for better visualization
            cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)

            # Draw a line between the thumb and index finger tips for better control
            cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)

            # Calculate the 3D distance between the thumb and index finger tips
            distance = calculate_3d_distance(thumb_tip.x, thumb_tip.y, thumb_tip.z, index_tip.x, index_tip.y, index_tip.z)

            # Get the hand label (left or right)
            hand_label = handedness.classification[0].label

            # Store thumb coordinates
            hand_landmarks[hand_label] = (thumb_x, thumb_y)

            # Control volume or brightness based on hand label
            if hand_label == "Left":
                min_distance = 0.05
                max_distance = 0.25
                volume_level = (distance - min_distance) / (max_distance - min_distance)  # For calculating volume level
                volume_level = max(0.0, min(1.0, volume_level))  # Volume level must be between 0 and 1 (%0 - %100)

                volume.SetMasterVolumeLevelScalar(volume_level, None)  # Set system volume

                # Display volume level on the screen
                cv2.putText(img, f"Volume: {int(volume_level * 100)}%", (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                # Draw vertical volume bar (red)
                bar_width = 20
                bar_height = 200
                bar_x = 50
                bar_y = 150
                cv2.rectangle(img, (bar_x, bar_y + int((1 - volume_level) * bar_height)), (bar_x + bar_width, bar_y + bar_height), (0, 0, 255), cv2.FILLED)
                cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 0, 255), 2)

            elif hand_label == "Right":
                min_distance = 0.05
                max_distance = 0.25
                brightness_level = (distance - min_distance) / (max_distance - min_distance)
                brightness_level = max(0.0, min(1.0, brightness_level))

                sbc.set_brightness(int(brightness_level * 100))  # Set screen brightness

                # Display brightness level on the screen (right side)
                cv2.putText(img, f"Brightness: {int(brightness_level * 100)}%", (img.shape[1] - 290, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

                # Draw vertical brightness bar (yellow)
                bar_width = 20
                bar_height = 200
                bar_x = img.shape[1] - 70
                bar_y = 150
                cv2.rectangle(img, (bar_x, bar_y + int((1 - brightness_level) * bar_height)), (bar_x + bar_width, bar_y + bar_height), (0, 255, 255), cv2.FILLED)
                cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 255, 255), 2)       

        # Check if both thumbs are touching (use 2D distance)
        if "Left" in hand_landmarks and "Right" in hand_landmarks:
            left_thumb_x, left_thumb_y = hand_landmarks["Left"]
            right_thumb_x, right_thumb_y = hand_landmarks["Right"]

            # Calculate 2D distance between both thumbs
            thumb_distance = calculate_2d_distance(left_thumb_x, left_thumb_y, right_thumb_x, right_thumb_y)

            # If thumbs are very close, exit the program
            if thumb_distance < 30:  # Adjust threshold as needed (2d)
                cv2.putText(img, "Exiting...", (img.shape[1] // 2 - 100, img.shape[0] // 2), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                cv2.imshow("Hand Gesture Control", img)
                cv2.waitKey(1000)  # Show message for 1 second
                break

    cv2.imshow("Hand Gesture Control", img)  # Display the image

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()