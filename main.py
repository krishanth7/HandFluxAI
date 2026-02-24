import cv2
import time
import pyautogui
import json
import os
import logging
from src.hand_tracker import HandTracker
from src.gesture_recognizer import GestureRecognizer
from src.action_controller import ActionController
from src.utils import calculate_distance

# Configure Corporate Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("handflux_system.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("HandFluxAI")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Configuration load failed: {e}")
        return None

def draw_premium_hud(img, gesture, fps):
    """Draw a professional, minimalist HUD overlay."""
    h, w, _ = img.shape
    
    # 1. Status Bar (Top Left)
    cv2.rectangle(img, (20, 20), (320, 110), (45, 45, 45), -1) # Dark background
    cv2.rectangle(img, (20, 20), (320, 110), (200, 200, 200), 1) # Border
    
    # Text Details
    cv2.putText(img, "HandFluxAI v1.0", (35, 45), 
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255), 1)
    cv2.putText(img, f"FPS: {int(fps)}", (35, 70), 
                cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    
    gesture_color = (0, 255, 0) if gesture != "None" else (100, 100, 100)
    cv2.putText(img, f"INTENT: {gesture}", (35, 95), 
                cv2.FONT_HERSHEY_DUPLEX, 0.6, gesture_color, 1)

    # 2. Bottom Instruction Bar
    cv2.rectangle(img, (20, h - 50), (w - 20, h - 10), (45, 45, 45), -1)
    cv2.putText(img, "SYTEM ACTIVE | PRESS 'Q' TO INITIALIZE SHUTDOWN", (w // 2 - 200, h - 25), 
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (180, 180, 180), 1)

def main():
    config = load_config()
    if not config:
        return

    logger.info("Initializing HandFluxAI Corporate Engine...")
    
    # Initialize Components
    cap = cv2.VideoCapture(config['camera']['id'])
    cap.set(3, config['camera']['width'])
    cap.set(4, config['camera']['height'])
    
    tracker = HandTracker(detection_con=config['detection']['min_confidence'])
    recognizer = GestureRecognizer()
    
    sw, sh = pyautogui.size()
    controller = ActionController(sw, sh)
    
    prev_time = 0
    logger.info("HandFluxAI initialized successfully. Interface active.")

    while True:
        success, img = cap.read()
        if not success:
            logger.error("Camera stream disconnected or inaccessible.")
            break
            
        img = cv2.flip(img, 1)
        
        # Perception Cycle
        img = tracker.find_hands(img, draw=False)
        lm_list = tracker.get_position(img, draw=False)
        
        current_gesture = "None"
        
        if lm_list:
            # Intelligence Cycle
            fingers = tracker.fingers_up(lm_list)
            current_gesture = recognizer.detect_gesture(lm_list, fingers)
            
            # Action Cycle
            controller.perform_action(current_gesture, lm_list, img.shape)
            
            # Draw professional landmark points
            for lm in lm_list:
                cv2.circle(img, (lm[1], lm[2]), 3, (0, 255, 255), -1)

        # Telemetry & UI
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time
        
        draw_premium_hud(img, current_gesture, fps)

        # Output
        cv2.imshow("HandFluxAI Corporate Interface", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("User initiated system shutdown.")
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("System offline.")

if __name__ == "__main__":
    main()
