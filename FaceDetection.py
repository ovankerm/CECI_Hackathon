import cv2
from detections import face_detector_singleplayer, face_detection_utils

if __name__ == "__main__":
	cap = cv2.VideoCapture(0)
	fdu = face_detection_utils(cap)
	print(face_detector_singleplayer(fdu))


