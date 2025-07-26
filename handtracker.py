import cv2
import numpy as np

cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)

# Skin color thresholds in YCrCb
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

    cont, _ = cv2.findContours(skinMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if cont:
        handCont = max(cont, key=cv2.contourArea)

        if cv2.contourArea(handCont) > 1000:
            # Draw green hand contour
            cv2.drawContours(frame, [handCont], -1, (0, 255, 0), 2)

            # Convex Hull (blue)
            hull = cv2.convexHull(handCont)
            cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)

            # Convexity Defects
            hullIndices = cv2.convexHull(handCont, returnPoints=False)
            defects = cv2.convexityDefects(handCont, hullIndices)

            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]

                    start = tuple(handCont[s][0])  # Fingertip
                    end = tuple(handCont[e][0])
                    far = tuple(handCont[f][0])   # Valley
                    depth = d

                    if depth > 10000:
                        # Draw red circle at fingertip
                        cv2.circle(frame, start, 6, (0, 0, 255), -1)

                        # Draw yellow circle at valley
                        cv2.circle(frame, far, 5, (0, 255, 255), -1)

                        # Optional: connect fingertip-to-fingertip
                        # cv2.line(frame, start, end, (255, 255, 255), 1)

    # Display windows
    cv2.imshow("Hand Tracker", frame)
    cv2.imshow("Skin Mask", skinMask)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
