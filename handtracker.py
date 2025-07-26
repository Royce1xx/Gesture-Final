import cv2
import numpy as np




cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(0)


lowerSkin = np.array([0, 133, 77], dtype=np.uint8)
upperSkin = np.array([255, 173, 127], dtype=np.uint8)




while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    colorConvert = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    skinMask = cv2.inRange(colorConvert, lowerSkin, upperSkin)


    skinMask = cv2.GaussianBlur(skinMask, (5, 5), 0)


    cv2.imshow("Hand Tracker", frame)
    cv2.imshow("Skin Mask", skinMask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   

