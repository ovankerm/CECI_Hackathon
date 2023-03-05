import cv2
import dlib
from scipy.spatial import distance
import mediapipe as mp
import time
from imutils import face_utils


class face_detection_utils:
    def __init__(self, cap):
        self.cap = cap
        self.face_detector = dlib.get_frontal_face_detector()
        self.facelandmark_processor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.min_AR_eye = 0.2
        self.min_AR_mouth = 0.76
        self.treshold = 10
        self.waitKey = 10

        success, img = cap.read()
        img_height, self.img_width, _ = img.shape
        self.img_height = int(img_height)
        self.half_img_width = int(self.img_width / 2)

        self.l_eye_counter = 0
        self.l_mouth_counter = 0
        self.r_eye_counter = 0
        self.r_mouth_counter = 0

        self.result = [[False, False], [False, False]]


class hands_detection_utils:
    def __init__(self, cap):
        self.cap = cap
        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(max_num_hands=4)
        self.mp_drawing_utils = mp.solutions.drawing_utils
        self.treshold = 20
        self.waitKey = 10

        self.counter = [0, 0, 0]


def compute_eye_aspect_ratio(eye):
    a = distance.euclidean(eye[1], eye[5])
    b = distance.euclidean(eye[2], eye[4])
    c = distance.euclidean(eye[0], eye[3])
    aspect_ratio = (a + b) / (2.0 * c)
    return aspect_ratio


def compute_mouth_aspect_ratio(mouth):
    a = distance.euclidean(mouth[2], mouth[10])
    b = distance.euclidean(mouth[4], mouth[8])
    c = distance.euclidean(mouth[0], mouth[6])
    aspect_ratio = (a + b) / (2.0 * c)
    return aspect_ratio


lStart, lEnd = 36, 42
rStart, rEnd = 42, 48
mStart, mEnd = 49, 68


def face_detector_multiplayer(fdu: face_detection_utils):
    while fdu.cap.isOpened():
        face_detector_singleIMG_multi(fdu)


def face_detector_singleIMG_multi(fdu: face_detection_utils):
    success, img = fdu.cap.read()
    if not success:
        return 0

    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_processed = fdu.face_detector(rgb_img)

    for single_face in faces_processed:
        single_face_landmarks = fdu.facelandmark_processor(rgb_img, single_face)
        face_landmarks_np = face_utils.shape_to_np(single_face_landmarks)

        left_eye = face_landmarks_np[lStart:lEnd]
        right_eye = face_landmarks_np[rStart:rEnd]
        left_AR = compute_eye_aspect_ratio(left_eye)
        right_AR = compute_eye_aspect_ratio(right_eye)
        eye_AR = min(left_AR, right_AR)

        mouth = face_landmarks_np[mStart:mEnd]
        mouth_AR = compute_mouth_aspect_ratio(mouth)

        nose = face_landmarks_np[29]
        x_rel = nose[0] / fdu.img_width

        if x_rel > 0.55:
            # Left player
            if eye_AR < fdu.min_AR_eye:
                fdu.l_eye_counter += 1
            else:
                fdu.l_eye_counter = 0
            if mouth_AR > fdu.min_AR_mouth:
                fdu.l_mouth_counter += 1
            else:
                fdu.l_mouth_counter = 0
            fdu.result[0][0] = fdu.l_eye_counter >= fdu.treshold
            fdu.result[0][1] = fdu.l_mouth_counter >= fdu.treshold

        if x_rel < 0.45:
            # Right player
            if left_AR < fdu.min_AR_eye or right_AR < fdu.min_AR_eye:
                fdu.r_eye_counter += 1
            else:
                fdu.r_eye_counter = 0
            if mouth_AR > fdu.min_AR_mouth:
                fdu.r_mouth_counter += 1
            else:
                fdu.r_mouth_counter = 0
            fdu.result[1][0] = fdu.r_eye_counter >= fdu.treshold
            fdu.result[1][1] = fdu.r_mouth_counter >= fdu.treshold

    # print([fdu.l_eye_counter, fdu.l_mouth_counter, fdu.r_eye_counter, fdu.r_mouth_counter])

    cv2.line(img, (fdu.half_img_width, 0), (fdu.half_img_width, fdu.img_height), (0, 0, 255), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(fdu.waitKey)


def face_detector_singleplayer(fdu: face_detection_utils):
    while fdu.cap.isOpened():
        face_detector_singleIMG_single(fdu)


def face_detector_singleIMG_single(fdu: face_detection_utils):
    success, img = fdu.cap.read()
    if not success:
        return 0
    img = cv2.flip(img, 1)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_processed = fdu.face_detector(rgb_img)

    for single_face in faces_processed:
        single_face_landmarks = fdu.facelandmark_processor(rgb_img, single_face)
        face_landmarks_np = face_utils.shape_to_np(single_face_landmarks)

        left_eye = face_landmarks_np[lStart:lEnd]
        right_eye = face_landmarks_np[rStart:rEnd]
        left_AR = compute_eye_aspect_ratio(left_eye)
        right_AR = compute_eye_aspect_ratio(right_eye)
        eye_AR = min(left_AR, right_AR)

        mouth = face_landmarks_np[mStart:mEnd]
        mouth_AR = compute_mouth_aspect_ratio(mouth)

        if eye_AR < fdu.min_AR_eye:
            fdu.l_eye_counter += 1
        else:
            fdu.l_eye_counter = 0
        if mouth_AR > fdu.min_AR_mouth:
            fdu.l_mouth_counter += 1
        else:
            fdu.l_mouth_counter = 0
        fdu.result[0][0] = fdu.l_eye_counter >= fdu.treshold
        fdu.result[0][1] = fdu.l_mouth_counter >= fdu.treshold

    cv2.imshow("Image", img)
    cv2.waitKey(fdu.waitKey)

def process_single_img_fingers(hdu: hands_detection_utils):
    success, img = hdu.cap.read()
    img = cv2.flip(img, 1)
    if not success:
        return 0

    hand_processed = hdu.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    all_hand_landmarks = hand_processed.multi_hand_landmarks

    if all_hand_landmarks:
        for single_hand_landmark in all_hand_landmarks:
            handIndex = hand_processed.multi_hand_landmarks.index(single_hand_landmark)
            handLabel = hand_processed.multi_handedness[handIndex].classification[0].label

            # Add points to diplayed img
            hdu.mp_drawing_utils.draw_landmarks(img, single_hand_landmark, hdu.mp_hand.HAND_CONNECTIONS)

            # Labels = ["Right", "Left"]
            # Attention a cause de la webcam, les mains sont inversées
            if handLabel == "Right":
                single_hand_landmark_xyz = single_hand_landmark.landmark

                if single_hand_landmark_xyz[4].y > single_hand_landmark_xyz[1].y:
                    hdu.counter[0] = 0
                    hdu.counter[1] = 0
                    hdu.counter[2] += 1
                else:
                    # Check if Ring finger or Pinky is down
                    if not (single_hand_landmark_xyz[16].y < single_hand_landmark_xyz[14].y or single_hand_landmark_xyz[
                        20].y < single_hand_landmark_xyz[18].y):

                        # Check if index is up
                        if single_hand_landmark_xyz[8].y < single_hand_landmark_xyz[6].y:

                            # Check if middle finger is up
                            if single_hand_landmark_xyz[12].y < single_hand_landmark_xyz[10].y:
                                hdu.counter[0] = 0
                                hdu.counter[1] += 1
                                hdu.counter[2] = 0
                            else:
                                hdu.counter[0] += 1
                                hdu.counter[1] = 0
                                hdu.counter[2] = 0

                    else:
                        hdu.counter[0] = 0
                        hdu.counter[1] = 0
                        hdu.counter[2] = 0
    cv2.imshow("Image", img)
    cv2.waitKey(hdu.waitKey)