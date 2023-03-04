import cv2
import mediapipe as mp

mp_hand = mp.solutions.hand

hands = mp_hand.Hand()

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    if not success:
        break
    cv2.imshow("Image", img)
    cv2.waitKey(10)  # Waits 10 ms

cap.release()
cv2.destroyAllWindows()

