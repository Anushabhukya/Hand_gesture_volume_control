import cv2
import mediapipe as mp


class handDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=mode,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    def findHands(self, img, draw=True):
        """Detect hands in a BGR image and optionally draw the skeleton."""
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS
                )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """Return (lmList, bbox).

        lmList: [[id, x, y], ...] in pixel coordinates (empty if no hand)
        bbox:   [xmin, ymin, xmax, ymax] (empty if no hand)
        """
        lmList = []
        bbox = []
        if self.results and self.results.multi_hand_landmarks:
            if handNo < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[handNo]
                h, w, _ = img.shape
                xs, ys = [], []
                for id, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xs.append(cx)
                    ys.append(cy)
                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                bbox = [min(xs), min(ys), max(xs), max(ys)]
        return lmList, bbox
