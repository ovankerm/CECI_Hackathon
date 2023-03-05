import copy

import cv2
import mediapipe as mp
import time
import numpy as np

mp_hand = mp.solutions.hands
hands = mp_hand.Hands(max_num_hands=4)
mp_drawing_utils = mp.solutions.drawing_utils

def analyze_img(cap, treshold = 20, wait_time = 10):
    """
    :param cap: VideoCapture cap = cv2.VideoCapture(0)
    :param treshold: Number of images necessary to validate the choice
    :param wait_time: Waiting time between each itration of the loop
    :return: Number of players validated, 1 or 2 (0 if error)
    """
    prev_time = time.time() # Used for FPS calculation
    finger_counter = np.zeros(2)
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            return 0

        process_img_fingers(img, finger_counter)
        # print(finger_counter)


        # FPS counter
        cur_time = time.time()
        FPS = int(1 / (cur_time - prev_time))
        prev_time = cur_time

        # print(FPS)
        if finger_counter[0] > treshold:
            return 1
        elif finger_counter[1] > treshold:
            return 2

        cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        cv2.imshow("Image", img)
        cv2.waitKey(wait_time)  # Waits wait_time ms

def process_img_fingers(img, counter):
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
                print(single_hand_landmark_xyz[0])

                # Check if Ring finger or Pinky is down
                if not (single_hand_landmark_xyz[16].y < single_hand_landmark_xyz[14].y or single_hand_landmark_xyz[
                    20].y < single_hand_landmark_xyz[18].y):

                    # Check if index is up
                    if single_hand_landmark_xyz[8].y < single_hand_landmark_xyz[6].y:

                        # Check if middle finger is up
                        if single_hand_landmark_xyz[12].y < single_hand_landmark_xyz[10].y:
                            counter[0] = 0
                            counter[1] += 1
                        else:
                            counter[0] += 1
                            counter[1] = 0

                else:
                    counter[0] = 0
                    counter[1] = 0




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


def hand_to_jump(cap, list_func, treshold = 20, wait_time = 10):
    prev_time = time.time()  # Used for FPS calculation
    old_mean_y_position = [0, 0]  # Used to store latest mean position [Left player, Right player]
    dy_required = 20   # Distance required to consider a jump
    dy_required /= 100

    latest_y_positions = np.zeros((treshold, 2))
    idx = 0

    while cap.isOpened():
        success, img = cap.read()
        # img = cv2.GaussianBlur(img, (15, 15), 0)
        if not success:
            return 0
        hand_processed = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        all_hand_landmarks = hand_processed.multi_hand_landmarks

        if all_hand_landmarks:
            left_hands_x_pos = [(0,0),(0,0)]
            fingers_up = [False, False]
            i = 0
            left_hand_present = False

            for single_hand_landmark in all_hand_landmarks:
                fingerCount = 0
                handIndex = hand_processed.multi_hand_landmarks.index(single_hand_landmark)
                handLabel = hand_processed.multi_handedness[handIndex].classification[0].label

                # Only looking at left hands
                if handLabel == "Right":
                    left_hand_present = True
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
                    try:
                        fingers_up[i] = fingerCount > 3
                        left_hands_x_pos[i] = (single_hand_landmark_xyz[0].x, single_hand_landmark_xyz[0].y)
                        i += 1
                    except IndexError:
                        print("Too many left hands")
            if left_hand_present:
                # First hand most on the left
                if left_hands_x_pos[0][0] > left_hands_x_pos[1][0]:
                    latest_y_positions[idx] = left_hands_x_pos[0][1], left_hands_x_pos[1][1]
                else:
                    latest_y_positions[idx] = left_hands_x_pos[1][1], left_hands_x_pos[0][1]
                idx += 1
                # print(old_mean_y_position)
                if idx >= treshold - 1:
                    mean_y_position = [np.mean(latest_y_positions[:,0]), np.mean(latest_y_positions[:,1])]
                    if old_mean_y_position[0] - mean_y_position[0] > dy_required:
                        print("Player 1 Jump")
                    if old_mean_y_position[1] - mean_y_position[1] > dy_required:
                        print("Player 2 Jump")
                    old_mean_y_position = copy.deepcopy(mean_y_position)
                    latest_y_positions = np.zeros((treshold, 2))
                    idx = 0


        # mp_drawing_utils.draw_landmarks(img, single_hand_landmark, mp_hand.HAND_CONNECTIONS)
        cv2.imshow("Image", img)
        cv2.waitKey(10)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print(hand_to_jump(cap, 20, 10))




