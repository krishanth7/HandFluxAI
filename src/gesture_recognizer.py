from .utils import calculate_distance

class GestureRecognizer:
    def __init__(self):
        self.points = {
            'THUMB_TIP': 4,
            'INDEX_TIP': 8,
            'MIDDLE_TIP': 12,
            'RING_TIP': 16,
            'PINKY_TIP': 20,
            'THUMB_IP': 3,
            'INDEX_MCP': 5
        }

    def detect_gesture(self, lm_list, fingers):
        if not lm_list:
            return "None"

        # 1. Cursor Move (Index finger up only or Index+Middle up)
        if fingers[1] == 1 and fingers[2] == 0:
            return "MOVE"
        
        # 2. Left Click (Index and Thumb touching/near)
        if fingers[1] == 1 and fingers[0] == 0: # Check distance instead
            dist = calculate_distance(lm_list[4][1:], lm_list[8][1:])
            if dist < 40:
                return "CLICK"

        # 3. Right Click (Middle and Thumb touching)
        if fingers[2] == 1:
            dist = calculate_distance(lm_list[4][1:], lm_list[12][1:])
            if dist < 40:
                return "RIGHT_CLICK"

        # 4. Volume Control (Pinch with Thumb and Index, but Middle also up)
        if fingers[1] == 1 and fingers[2] == 1:
             # If index and middle are up, maybe it's scroll or volume
             dist = calculate_distance(lm_list[8][1:], lm_list[12][1:])
             if dist < 40:
                 return "HOVER_SELECT" # Or something else
        
        # 5. Scroll Up/Down
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            return "SCROLL"

        # 6. Pause/Play (Fist - all fingers down)
        if sum(fingers) == 0:
            return "PAUSE"

        return "NEUTRAL"
