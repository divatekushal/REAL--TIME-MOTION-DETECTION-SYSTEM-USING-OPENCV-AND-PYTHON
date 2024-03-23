import cv2
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
from plyer import notification

# Directory to save motion event images
output_directory = "motion_images"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define the maximum age (in days) of files to keep
max_age_days = 1  # Adjust as needed

# Define the ROI (Region of Interest) coordinates
roi_x, roi_y, roi_width, roi_height = 100, 100, 200, 200

# Initialize the GUI
root = tk.Tk()
root.title("Motion Detection")

# Flag to control motion detection
stop_motion = False

# List to store the last 10 motion detection timestamps
motion_history = []

# Function to update the motion history listbox
def update_motion_history():
    history_listbox.delete(0, tk.END)  # Clear the listbox
    for timestamp in motion_history:
        history_listbox.insert(tk.END, timestamp)

# Function to show a pop-up notification
def show_notification():
    notification_title = "Motion Detected"
    notification_message = "Motion has been detected!"
    notification.app_name = "Motion Detection App"
    notification_timeout = 5  # Display notification for 5 seconds

    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=notification_timeout
    )

# Function to start motion detection
def start_motion_detection():
    global stop_motion
    stop_motion = False

    # Disable the Start button
    start_button["state"] = "disabled"

    # Enable the Stop button
    stop_button["state"] = "normal"

    # Start motion detection in a separate thread
    motion_detection_thread = threading.Thread(target=motion_detection)
    motion_detection_thread.start()

# Function to stop motion detection
def stop_motion_detection():
    global stop_motion
    stop_motion = True

# Function to perform motion detection
def motion_detection():
    # capturing video in real time
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera.")
        return

    while not stop_motion:
        # Reading frames sequentially
        ret, frame1 = cap.read()
        if not ret:
            messagebox.showerror("Error", "Could not read frame 1.")
            break

        ret, frame2 = cap.read()
        if not ret:
            messagebox.showerror("Error", "Could not read frame 2.")
            break

        # Difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False  # Flag to track motion detection

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            # Check if the motion is within the ROI
            if roi_x < x < (roi_x + roi_width) and roi_y < y < (roi_y + roi_height):
                if cv2.contourArea(contour) < 900:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Add timestamp to the image
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cv2.putText(frame1, f"STATUS: MOTION DETECTED ({timestamp})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

                motion_detected = True  # Set motion detected flag to True

                # Save the frame as an image when motion is detected
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_filename = os.path.join(output_directory, f"motion_{timestamp}.jpg")
                cv2.imwrite(image_filename, frame1)

                # Show pop-up notification
                

                # Add the timestamp to the motion history list
                motion_history.append(timestamp)
                if len(motion_history) > 10:
                    motion_history.pop(0)  # Remove the oldest timestamp

                # Update the motion history listbox
                update_motion_history()

        cv2.imshow("Video", frame1)
        frame1 = frame2

        if motion_detected:
            print("Motion Detected!")

        if cv2.waitKey(50) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Enable the Start button
    start_button["state"] = "normal"

    # Disable the Stop button
    stop_button["state"] = "disabled"

# Create Start button
start_button = ttk.Button(root, text="Start Motion Detection", command=start_motion_detection)
start_button.pack(pady=10)
start_button["state"] = "normal"

# Create Stop button
stop_button = ttk.Button(root, text="Stop Motion Detection", command=stop_motion_detection)
stop_button.pack(pady=10)
stop_button["state"] = "disabled"

# Create Quit button
quit_button = ttk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(pady=10)

# Create motion history listbox
history_listbox = tk.Listbox(root, height=10)
history_listbox.pack(pady=10)
update_motion_history()  # Initialize the listbox with the existing motion history

root.mainloop()
