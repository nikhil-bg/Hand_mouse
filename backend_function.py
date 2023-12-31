import cv2
import mediapipe as mp
import pyautogui
import math

cap = cv2.VideoCapture(0)
hand_detect = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0


smoothing_factor = 5 
smooth_thumb_x, smooth_thumb_y = 0, 0
smooth_index_x, smooth_index_y = 0, 0

thumb_index_touching = False 

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detect.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y


            smooth_thumb_x += (thumb_x - smooth_thumb_x) / smoothing_factor
            smooth_thumb_y += (thumb_y - smooth_thumb_y) / smoothing_factor
            smooth_index_x += (index_x - smooth_index_x) / smoothing_factor
            smooth_index_y += (index_y - smooth_index_y) / smoothing_factor

            distance = math.sqrt((smooth_thumb_x - smooth_index_x) ** 2 + (smooth_thumb_y - smooth_index_y) ** 2)
            if distance < 40:
                thumb_index_touching = True
            else:
                thumb_index_touching = False

            if thumb_index_touching:
                pyautogui.click()

            if smooth_index_y < smooth_thumb_y - 45:  # Until it hits 45, thumb is not raised (not clicked). You can adjust it bro based on your finger distance. 
                pyautogui.moveTo(smooth_index_x, smooth_index_y)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
 
