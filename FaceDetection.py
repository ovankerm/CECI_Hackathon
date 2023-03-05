import cv2
import dlib
from scipy.spatial import distance
import time
from imutils import face_utils

def compute_eye_aspect_ratio(eye):
	a = distance.euclidean(eye[1], eye[5])
	b = distance.euclidean(eye[2], eye[4])
	c = distance.euclidean(eye[0], eye[3])
	aspect_ratio = (a+b)/(2.0*c)
	return aspect_ratio

def compute_mouth_aspect_ratio(mouth):
	a = distance.euclidean(mouth[2], mouth[10])
	b = distance.euclidean(mouth[4], mouth[8])
	c = distance.euclidean(mouth[0], mouth[6])
	aspect_ratio = (a+b)/(2.0*c)
	return aspect_ratio


lStart, lEnd = 36, 42
rStart, rEnd = 42, 48
mStart, mEnd = 49, 68

def face_detector_multiplayer(cap, lst, treshold = 10):
	prev_time = time.time()  # Used for FPS calculation

	face_detector = dlib.get_frontal_face_detector()
	facelandmark_processor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	min_AR_eye = 0.2
	min_AR_mouth = 0.76

	success, img = cap.read()
	img_height, img_width, _ = img.shape
	img_height = int(img_height)
	half_img_width = int(img_width/2)

	l_eye_counter = 0
	l_mouth_counter = 0

	r_eye_counter = 0
	r_mouth_counter = 0

	while cap.isOpened():
		success, img = cap.read()
		if not success:
			return 0

		rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces_processed = face_detector(rgb_img)

		# FPS counter
		cur_time = time.time()
		FPS = int(1 / (cur_time - prev_time))
		prev_time = cur_time

		for single_face in faces_processed:
			single_face_landmarks = facelandmark_processor(rgb_img, single_face)
			face_landmarks_np = face_utils.shape_to_np(single_face_landmarks)

			left_eye = face_landmarks_np[lStart:lEnd]
			right_eye = face_landmarks_np[rStart:rEnd]
			left_AR = compute_eye_aspect_ratio(left_eye)
			right_AR = compute_eye_aspect_ratio(right_eye)
			eye_AR = min(left_AR, right_AR)

			mouth = face_landmarks_np[mStart:mEnd]
			mouth_AR = compute_mouth_aspect_ratio(mouth)

			nose = face_landmarks_np[29]
			x_rel = nose[0] / img_width

			if x_rel > 0.55:
				# cv2.line(img, (0, 200), (320, 200), (0, 0, 255), 10)
				# Left player
				if eye_AR < min_AR_eye:
					l_eye_counter += 1
				else:
					l_eye_counter = 0
				if mouth_AR > min_AR_mouth:
					l_mouth_counter += 1
				else:
					l_mouth_counter = 0
				lst[0][0] = l_eye_counter >= treshold
				lst[0][1] = l_mouth_counter >= treshold

			if x_rel < 0.45:
				# cv2.line(img, (320, 200), (640, 200), (0, 0, 255), 10)
				# Right player
				if left_AR < min_AR_eye or right_AR < min_AR_eye:
					r_eye_counter += 1
				else:
					r_eye_counter = 0
				if mouth_AR > min_AR_mouth:
					r_mouth_counter += 1
				else:
					r_mouth_counter = 0
				lst[1][0] = r_eye_counter >= treshold
				lst[1][1] = r_mouth_counter >= treshold


		"""if lst[1][0]:
			cv2.line(img, (0,10), (320,10), (0, 0, 255), 10)
		if lst[1][1]:
			cv2.line(img, (0, 480), (320, 480), (255, 0, 0), 10)

		if lst[0][0]:
			cv2.line(img, (320,10), (640,10), (0, 0, 255), 10)
		if lst[0][1]:
			cv2.line(img, (320, 480), (640, 480), (255, 0, 0), 10)"""
			# print(single_face_landmarks.part(0))

			#print(len(single_face_landmarks))

		cv2.line(img, (half_img_width,0), (half_img_width,img_height), (0, 0, 255), 5)
		cv2.imshow("Image", img)
		cv2.waitKey(1)

def face_detector_singleplayer(cap, lst, treshold = 10):
	prev_time = time.time()  # Used for FPS calculation

	face_detector = dlib.get_frontal_face_detector()
	facelandmark_processor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	min_AR_eye = 0.15
	min_AR_mouth = 0.76

	eye_counter = 0
	mouth_counter = 0

	while cap.isOpened():
		success, img = cap.read()
		if not success:
			return 0

		rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces_processed = face_detector(rgb_img)

		# FPS counter
		cur_time = time.time()
		FPS = int(1 / (cur_time - prev_time))
		prev_time = cur_time

		for single_face in faces_processed:
			single_face_landmarks = facelandmark_processor(rgb_img, single_face)
			face_landmarks_np = face_utils.shape_to_np(single_face_landmarks)

			left_eye = face_landmarks_np[lStart:lEnd]
			right_eye = face_landmarks_np[rStart:rEnd]
			left_AR = compute_eye_aspect_ratio(left_eye)
			right_AR = compute_eye_aspect_ratio(right_eye)

			mouth = face_landmarks_np[mStart:mEnd]
			mouth_AR = compute_mouth_aspect_ratio(mouth)

			if left_AR < min_AR_eye or right_AR < min_AR_eye:
				eye_counter += 1
			else:
				eye_counter = 0
			if mouth_AR > min_AR_mouth:
				mouth_counter += 1
			else:
				mouth_counter = 0

			lst[0] = eye_counter >= treshold
			lst[1] = mouth_counter >= treshold

		if lst[0]:
			cv2.line(img, (0,10), (640,10), (0, 0, 255), 10)
		if lst[1]:
			cv2.line(img, (0, 480), (640, 480), (255, 0, 0), 10)

		cv2.putText(img, f"{FPS} FPS", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

		cv2.imshow("Image", img)
		cv2.waitKey(1)

if __name__ == "__main__":
	#ORIGINAL()
	cap = cv2.VideoCapture(0)
	lst = [[False, False], [False, False]]
	print(face_detector_multiplayer(cap, lst))


