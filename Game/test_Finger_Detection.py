import cv2
import mediapipe as mp
import time

from Finger_Detection import hands_up, analyze_img



def __test_hand_up():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            return 0
        print(hands_up(img))

def __test_analyze_img():
    cap = cv2.VideoCapture(0)
    print(analyze_img(cap, treshold=50, wait_time=1))
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    __test_analyze_img()
