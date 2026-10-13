# Hand Gesture Volume Control System ✋🔊

A real-time computer vision project that allows users to control their Windows system volume using hand gestures through a webcam.

The system tracks the distance between the thumb and index finger using MediaPipe and OpenCV, then adjusts the system volume based on the detected distance.

## 📌 Project Overview

This project demonstrates how computer vision can be used for touchless human-computer interaction. Instead of manually adjusting the volume using a keyboard or mouse, users can control it by moving their fingers closer together or farther apart.

## ✨ Features

- Real-time hand detection and tracking
- Hand landmark visualization using MediaPipe
- Distance calculation between the thumb and index finger
- Gesture-based Windows system volume control
- Live webcam feed using OpenCV
- Modular Python code for hand tracking and volume control

## 🛠️ Technologies Used

- **Python 3.12**
- **OpenCV** – Webcam capture and image processing
- **MediaPipe** – Hand landmark detection
- **NumPy** – Numerical operations
- **Pycaw** – Windows system volume control
- **comtypes** – Windows COM interface support

## 📂 Project Structure

```text
Hand-Gesture-Volume-Control/
│
├── HandTrackingModule.py
├── VolumeHandControl.py
├── requirements.txt
├── .gitignore
├── README.md
└── screenshots/
    ├── volume-0.png
    └── volume-50.png
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Anushabhukya/Hand_gesture_volume_control.git
cd Hand_gesture_volume_control
```

### 2. Create a virtual environment

Python 3.12 is recommended for compatibility with the MediaPipe version used in this project.

```powershell
py -3.12 -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the required libraries

```bash
python -m pip install mediapipe==0.10.21 opencv-python numpy pycaw comtypes
```

### 5. Run the application

```bash
python VolumeHandControl.py
```

Allow webcam access if prompted.

## 🚀 How It Works

1. The webcam captures live video of the user's hand.
2. MediaPipe detects the hand and identifies its landmarks.
3. The program identifies the thumb tip and index finger tip.
4. The distance between these fingertips is calculated.
5. The distance is mapped to a volume range.
6. Pycaw adjusts the Windows system volume accordingly.

**Gesture control:**
- Fingers closer together → Lower volume
- Fingers farther apart → Higher volume

The exact distance-to-volume mapping depends on the implementation in `VolumeHandControl.py`.

## 📸 Project Screenshots

### Volume Control at 0%

When the thumb and index finger are close together, the program can set the system volume to 0%, depending on the configured distance mapping.

![Hand gesture volume control at 0 percent](screenshots/volume-0.png)

### Volume Control at 50%

At a moderate distance between the thumb and index finger, the program can set the system volume to approximately 50%, depending on the configured mapping.

![Hand gesture volume control at 50 percent](screenshots/volume-50.png)

*These screenshots should be captured from the actual running application, showing the hand landmarks and Windows volume indicator.*

## 💡 Applications

- Touchless computer interaction
- Gesture-based audio control
- Human-computer interaction
- Accessibility-oriented interfaces
- Computer vision experimentation

## 🔮 Future Improvements

- Add gesture-based mute and unmute functionality
- Display the current volume percentage on the webcam window
- Improve gesture stability and volume sensitivity
- Support additional hand gestures
- Extend gesture control to other desktop functions

## 👩‍💻 Author

**Anusha Bhukya**

GitHub: [Anushabhukya](https://github.com/Anushabhukya)

## 📄 License

This project is developed for educational and learning purposes.
