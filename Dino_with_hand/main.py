import cv2
import mediapipe as mp
import numpy as np
from pykeyboard import PyKeyboard
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def calculate_fingers(landmarks) -> int:
    sum = 0
    landmarks = np.array([[l.x, l.y, l.z] for l in landmarks])

    finger_p = (landmarks[9]+landmarks[13])/2-landmarks[0]
    for u, v, w in [[6, 7, 8], [10, 11, 12], [14, 15, 16], [18, 19, 20]]:
        finger1 = landmarks[v]-landmarks[u]
        finger2 = landmarks[w]-landmarks[v]
        if np.dot(finger1, finger_p) > 0 and np.dot(finger2, finger_p) > 0:
            sum += 1

    thumb_p = landmarks[5]-landmarks[9]
    thumb = landmarks[4]-landmarks[3]
    if np.dot(thumb, thumb_p) > 0:
        sum += 1
    return sum


def grab(landmarks) -> bool:
    '''判断五个手指尖所围成的面积是否比手掌心面积小'''
    landmarks = np.array([[l.x, l.y] for l in landmarks])
    # hull = cv2.convexHull(landmarks, True, returnpoints)
    fingers = landmarks[[4, 8, 12, 16, 20]].astype(np.float32)
    finger_area = cv2.contourArea(fingers)
    hand = landmarks[[0, 1, 5, 9, 13, 17]].astype(np.float32)
    hand_area = cv2.contourArea(hand)
    return finger_area < hand_area


def updown(landmarks) -> bool:
    '''最高的手指和手腕的距离大于拇指和小指的距离 且 最高的手指比手腕高'''
    landmarks = np.array([[l.x, l.y] for l in landmarks])
    # hull = cv2.convexHull(landmarks, True, returnpoints)
    return landmarks[0][1]-np.min(landmarks[[8, 12, 16, 20], 1]) > 0.5*abs(landmarks[4][0]-landmarks[20][0])


# For webcam input:
cap = cv2.VideoCapture(0)
keyboard = PyKeyboard()

##### 使用 Selenium 调出小恐龙 #####
driver = webdriver.Chrome()
# 忽略异常
try:
    driver.get('chrome://dino')
except WebDriverException:
    pass
####################################


with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                #### 三种控制方式 ####
                # if calculate_fingers(hand_landmarks.landmark)>3:
                # if updown(hand_landmarks.landmark):
                if not grab(hand_landmarks.landmark):
                    print('up')
                    keyboard.press_key(keyboard.space_key)
                else:
                    print('down')

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.

        #### 解除注释显示摄像头 ####
        # cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        # if cv2.waitKey(5) & 0xFF == 27:
        #     break
        ###########################
cap.release()
