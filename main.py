import cv2
import time
import pyautogui
import json
import os
from src.hand_tracker import HandTracker
from src.gesture_recognizer import GestureRecognizer
from src.action_controller import ActionController
from src.utils import calculate_distance

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    
    # 1. Initialize Components
    cap = cv2.VideoCapture(config['camera']['id'])
    cap.set(3, config['camera']['width'])
    cap.set(4, config['camera']['height'])
    
    tracker = HandTracker(detection_con=config['detection']['min_confidence'])
    recognizer = GestureRecognizer()
    
    sw, sh = pyautogui.size()
    controller = ActionController(sw, sh)
    
    prev_time = 0
    
    print("HandFluxAI Started. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to access camera.")
            break
            
        img = cv2.flip(img, 1) # Flip for selfie view
        
        # 2. Track Hand
        img = tracker.find_hands(img)
        lm_list = tracker.get_position(img, draw=False)
        
        if lm_list:
            # 3. Get Gesture
            fingers = tracker.fingers_up(lm_list)
            gesture = recognizer.detect_gesture(lm_list, fingers)
            
            # 4. Perform Action
            controller.perform_action(gesture, lm_list, img.shape)
            
            # Special Volume Control Action (Thumb-Index Distance)
            if fingers[0] == 1 and fingers[1] == 1 and sum(fingers) == 2:
                dist = calculate_distance(lm_list[4][1:], lm_list[8][1:])
                # Visual bar for volume feedback could go here
                cv2.putText(img, f"Vol Dist: {int(dist)}", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 5. UI Overlay
            cv2.putText(img, f"Gesture: {gesture}", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Highlight index tip if moving
            if gesture == "MOVE":
                cv2.circle(img, (lm_list[8][1], lm_list[8][2]), 15, (0, 255, 255), cv2.FILLED)

        # 6. FPS Calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(img, f"FPS: {int(fps)}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # 7. Display
        cv2.imshow("HandFluxAI - Gestures", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
