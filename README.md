**OVERVIEW**

This Python script leverages the OpenCV library to perform real-time motion detection using a computer's camera. The program captures consecutive video frames, computes the absolute difference between them, and identifies regions with significant changes to detect motion. When motion is detected, the affected areas are highlighted with bounding rectangles in the displayed video feed.

**KEY CONTRIBUTIONS**

->Real-Time Motion Detection: The script provides a real-time motion detection feature, making it suitable for applications that require immediate response to changes in the environment.

->Configurability: Users can easily customize the script by adjusting parameters such as the camera index, threshold value, and contour area threshold. This allows for fine-tuning the motion detection sensitivity based on specific use cases.


->Simple and Lightweight Implementation: The script offers a straightforward yet effective implementation of motion detection, making it accessible for users with varying levels of experience in computer vision.


->Bounding Rectangles Visualization: Detected motion is visually highlighted with bounding rectangles in the displayed video feed, providing a clear indication of areas with significant changes.


->Dependency on OpenCV and NumPy: Leveraging the power of OpenCV and NumPy, the script benefits from robust image processing capabilities and efficient numerical operations, ensuring reliable and efficient motion detection.

**DEPENDENCIES**

->OpenCV (cv2)

->NumPy (numpy)

**USAGE**

->Clone the repository or download the script.

->Install dependencies: pip install opencv-python numpy

->Run the script: python motion_detection.py

->The script will use the default camera (camera index 0) to capture video. Press the 'Esc' key to exit the program.

**LICENSE**

This project is licensed under the MIT License - see the LICENSE file for details.

**OUTCOME**

The motion detection script demonstrates a practical application of computer vision techniques, providing real-time identification of motion in live video. With a user-friendly and customizable design, the script offers adaptability for various scenarios. The clear visual feedback through bounding rectangles enhances the interpretation of detected motion areas. Leveraging the robust OpenCV and NumPy libraries ensures efficient image processing and numerical operations, resulting in a lightweight and responsive solution for motion detection tasks.
