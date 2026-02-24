import pyautogui
import numpy as np
from .utils import MovingAverage, calculate_distance

# Disable PyAutoGUI fail-safe to prevent crashes 
# (though it's recommended to keep it on, we'll configure it carefully)
pyautogui.FAILSAFE = True

class ActionController:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoother = MovingAverage(size=5)
        self.last_gesture = "None"
        self.click_cooldown = 0
        
    def perform_action(self, gesture, lm_list, frame_shape):
        h, w, c = frame_shape
        
        if gesture == "MOVE":
            # Extract index finger tip coordinates
            x_raw, y_raw = lm_list[8][1], lm_list[8][2]
            
            # Map coordinates to screen size (with some padding for comfort)
            # frame is w x h, screen is screen_width x screen_height
            # Add margin to avoid reaching the very edges of the frame to hit the screen edges
            margin = 100
            x = np.interp(x_raw, [margin, w - margin], [0, self.screen_width])
            y = np.interp(y_raw, [margin, h - margin], [0, self.screen_height])
            
            # Smooth the movement
            smooth_coords = self.smoother.update([x, y])
            pyautogui.moveTo(smooth_coords[0], smooth_coords[1])

        elif gesture == "CLICK":
            if self.last_gesture != "CLICK":
                pyautogui.click()
                
        elif gesture == "RIGHT_CLICK":
            if self.last_gesture != "RIGHT_CLICK":
                pyautogui.rightClick()

        elif gesture == "SCROLL":
            # Distance between index and middle could determine scroll speed?
            # Or just scroll based on y movement
            pyautogui.scroll(10) # Simple scroll up for demo

        elif gesture == "PAUSE":
            if self.last_gesture != "PAUSE":
                pyautogui.press('space')

        self.last_gesture = gesture

    def control_volume(self, dist):
        """Volume control based on pinch distance."""
        if dist > 200:
            pyautogui.press('volumeup')
        elif dist < 50:
            pyautogui.press('volumedown')
