import math
import time
from ctypes import POINTER, cast

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm

# ---------------- Camera setup ----------------
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # width
cap.set(4, hCam)  # height

if not cap.isOpened():
    raise RuntimeError("Could not open the camera. Check that it is connected and not in use.")

pTime = 0

# ---------------- Hand detector ----------------
detector = htm.handDetector(detectionCon=0.7)

# ---------------- Audio setup (Windows only) ----------------
devices = AudioUtilities.GetSpeakers()
try:
    # Older pycaw versions
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
except AttributeError:
    # Newer pycaw versions expose the endpoint volume directly
    volume = devices.EndpointVolume

volRange = volume.GetVolumeRange()  # e.g. (-65.25, 0.0, 0.03125)
minVol, maxVol = volRange[0], volRange[1]

# Distance between thumb and index finger (in pixels) mapped to volume
MIN_LENGTH, MAX_LENGTH = 50, 300

vol = 0
volBar = 400
volPer = 0

# ---------------- Main loop ----------------
while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from camera")
        break

    img = cv2.flip(img, 1)  # mirror the image
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]  # thumb tip
        x2, y2 = lmList[8][1], lmList[8][2]  # index finger tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # midpoint

        # Draw markers
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Distance between fingertips
        length = math.hypot(x2 - x1, y2 - y1)

        # Map distance to volume level, bar position and percentage
        vol = np.interp(length, [MIN_LENGTH, MAX_LENGTH], [minVol, maxVol])
        volBar = np.interp(length, [MIN_LENGTH, MAX_LENGTH], [400, 150])
        volPer = np.interp(length, [MIN_LENGTH, MAX_LENGTH], [0, 100])

        # Set system volume
        volume.SetMasterVolumeLevel(float(vol), None)

        # Fingers touching: highlight the midpoint
        if length < MIN_LENGTH:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(
        img, f"{int(volPer)} %", (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3
    )

    # FPS
    cTime = time.time()
    fps = 1 / max(cTime - pTime, 1e-6)
    pTime = cTime
    cv2.putText(
        img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3
    )

    cv2.imshow("Gesture Volume Control", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
