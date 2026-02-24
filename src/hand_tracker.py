import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

class HandTracker:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        # Model path
        self.model_path = "hand_landmarker.task"
        self._ensure_model_exists()

        # Initialize Hand Landmarker
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_con,
            min_hand_presence_confidence=track_con,
            running_mode=vision.RunningMode.IMAGE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None

    def _ensure_model_exists(self):
        """Download the model if it doesn't exist."""
        if not os.path.exists(self.model_path):
            print(f"Downloading MediaPipe hand model to {self.model_path}...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            urllib.request.urlretrieve(url, self.model_path)
            print("Download complete.")

    def find_hands(self, img, draw=True):
        """Find hands in the image and optionally draw landmarks."""
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Detect
        self.results = self.detector.detect(mp_image)

        if draw and self.results.hand_landmarks:
            for hand_lms in self.results.hand_landmarks:
                # Manual drawing since legacy mp_draw might be missing
                for lm in hand_lms:
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return img

    def get_position(self, img, hand_no=0, draw=True):
        """Get positions of all landmarks for a specific hand."""
        lm_list = []
        if self.results and self.results.hand_landmarks and hand_no < len(self.results.hand_landmarks):
            my_hand = self.results.hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lm_list

    def fingers_up(self, lm_list):
        """Returns which fingers are up (1) or down (0)."""
        if not lm_list:
            return []
            
        fingers = []
        # Tip landmarks: Thumb(4), Index(8), Middle(12), Ring(16), Pinky(20)
        tips = [8, 12, 16, 20]
        
        # Thumb - basic check (using x-coordinate relative to MCP joint for thumb)
        if lm_list[4][1] > lm_list[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers
        for id in tips:
            if lm_list[id][2] < lm_list[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
