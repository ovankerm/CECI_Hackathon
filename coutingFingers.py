import cv2
import mediapipe as mp

treshold = 20  # Number of image required before validation of the nbr of players

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()

mp_drawing_utils = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()

    if not success:
        break

    hand_processed = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #print(hand_processed.multi_hand_landmarks)
    fingerCount = 0
    all_hand_landmarks = hand_processed.multi_hand_landmarks

    if all_hand_landmarks:
        for single_hand_landmark in all_hand_landmarks:
            handIndex = hand_processed.multi_hand_landmarks.index(single_hand_landmark)
            handLabel = hand_processed.multi_handedness[handIndex].classification[0].label

            # Labels = ["Right", "Left"]
            # Attention a cause de la webcam, les mains sont inversées
            if handLabel == "Left":
                pass

            # Add points to diplayed img
            mp_drawing_utils.draw_landmarks(img, single_hand_landmark, mp_hand.HAND_CONNECTIONS)

            single_hand_landmark_xyz = single_hand_landmark.landmark

            if single_hand_landmark_xyz[8].y < single_hand_landmark_xyz[6].y:  # Index
                fingerCount += 1
            if single_hand_landmark_xyz[12].y < single_hand_landmark_xyz[10].y:  # Middle  finger
                fingerCount += 1
            if single_hand_landmark_xyz[16].y < single_hand_landmark_xyz[14].y:  # Ring finger
                fingerCount += 1
            if single_hand_landmark_xyz[20].y < single_hand_landmark_xyz[18].y:  # Pinky
                fingerCount += 1

    cv2.putText(img, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
    cv2.imshow("Image", img)
    cv2.waitKey(10)  # Waits 10 ms

cap.release()
cv2.destroyAllWindows()

