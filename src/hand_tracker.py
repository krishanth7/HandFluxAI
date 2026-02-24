import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        """Find hands in the image and optionally draw landmarks."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_position(self, img, hand_no=0, draw=True):
        """Get positions of all landmarks for a specific hand."""
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
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
        # Thumb (check if thumb tip is on left/right of IP joint depending on hand orientation)
        # Simplified: check x distance for horizontal movement or y for vertical
        # For simplicity, we'll use y-coordinate for all fingers except thumb
        
        # Tip landmarks: Thumb(4), Index(8), Middle(12), Ring(16), Pinky(20)
        tips = [8, 12, 16, 20]
        
        # Thumb - basic check
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
