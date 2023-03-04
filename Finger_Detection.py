import cv2
import mediapipe as mp
import time

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()
mp_drawing_utils = mp.solutions.drawing_utils

def analyze_img(cap, treshold = 20, wait_time = 10):
    """
    :param cap: VideoCapture cap = cv2.VideoCapture(0)
    :param treshold: Number of images necessary to validate the choice
    :param wait_time: Waiting time between each itration of the loop
    :return: Number of players validated, 1 or 2 (0 if error)
    """
    prev_time = time.time() # Used for FPS calculation



    two_finger_counter = 0
    one_finger_counter = 0
    while cap.isOpened():
        success, img = cap.read()
        img = cv2.GaussianBlur(img, (15, 15), 0)
        if not success:
            return 0

        hand_processed = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        all_hand_landmarks = hand_processed.multi_hand_landmarks

        if all_hand_landmarks:
            for single_hand_landmark in all_hand_landmarks:
                handIndex = hand_processed.multi_hand_landmarks.index(single_hand_landmark)
                handLabel = hand_processed.multi_handedness[handIndex].classification[0].label

                # Add points to diplayed img
                mp_drawing_utils.draw_landmarks(img, single_hand_landmark, mp_hand.HAND_CONNECTIONS)

                # Labels = ["Right", "Left"]
                # Attention a cause de la webcam, les mains sont inversées
                if handLabel == "Left":
                    single_hand_landmark_xyz = single_hand_landmark.landmark

                    # Check if Ring finger or Pinky is down
                    if not (single_hand_landmark_xyz[16].y < single_hand_landmark_xyz[14].y or single_hand_landmark_xyz[
                        20].y < single_hand_landmark_xyz[18].y):

                        # Check if index is up
                        if single_hand_landmark_xyz[8].y < single_hand_landmark_xyz[6].y:

                            # Check if middle finger is up
                            if single_hand_landmark_xyz[12].y < single_hand_landmark_xyz[10].y:
                                one_finger_counter = 0
                                two_finger_counter += 1
                                # print(f"two = {two_finger_counter}")
                                if two_finger_counter > treshold:
                                    return 2
                            else:
                                one_finger_counter += 1
                                two_finger_counter = 0
                                # print(f"one = {one_finger_counter}")
                                if one_finger_counter > treshold:
                                    return 1

                    else:
                        one_finger_counter = 0
                        two_finger_counter = 0
        # FPS counter
        cur_time = time.time()
        FPS = int(1 / (cur_time - prev_time))
        prev_time = cur_time

        # print(FPS)

        cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.imshow("Image", img)
        cv2.waitKey(wait_time)  # Waits wait_time ms



def hands_up(img):
    hand_processed = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    all_hand_landmarks = hand_processed.multi_hand_landmarks

    if all_hand_landmarks:
        for single_hand_landmark in all_hand_landmarks:
            fingerCount = 0
            handIndex = hand_processed.multi_hand_landmarks.index(single_hand_landmark)
            handLabel = hand_processed.multi_handedness[handIndex].classification[0].label

            # Add points to diplayed img
            mp_drawing_utils.draw_landmarks(img, single_hand_landmark, mp_hand.HAND_CONNECTIONS)

            single_hand_landmark_xyz = single_hand_landmark.landmark

            # Check if Ring finger or Pinky is down
            if single_hand_landmark_xyz[8].y < single_hand_landmark_xyz[6].y:  # Index
                fingerCount += 1
            if single_hand_landmark_xyz[12].y < single_hand_landmark_xyz[10].y:  # Middle  finger
                fingerCount += 1
            if single_hand_landmark_xyz[16].y < single_hand_landmark_xyz[14].y:  # Ring finger
                fingerCount += 1
            if single_hand_landmark_xyz[20].y < single_hand_landmark_xyz[18].y:  # Pinky
                fingerCount += 1
            if fingerCount > 3:
                # mp_drawing_utils.draw_landmarks(img, single_hand_landmark, mp_hand.HAND_CONNECTIONS)
                # cv2.imshow("Image", img)
                # cv2.waitKey(10)
                return True
    return False








