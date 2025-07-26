import cv2
import numpy as np
import math

cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)

lowerSkin = np.array([0, 133, 77], dtype=np.uint8)
upperSkin = np.array([255, 173, 127], dtype=np.uint8)


def extract_gesture_vector(contour, defects, frame_height):
    vector = []
    defect_depths = []
    defect_angles = []

    finger_count = 0

    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = contour[s][0]
            end = contour[e][0]
            far = contour[f][0]

            a = np.linalg.norm(start - far)
            b = np.linalg.norm(end - far)
            c = np.linalg.norm(end - start)

            if a == 0 or b == 0:
                continue

            angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b))

            # Accept only tight valleys between fingers
            if d > 5000 and angle < math.pi / 2 and far[1] < frame_height * 0.8:
                finger_count += 1
                defect_depths.append(int(d))
                defect_angles.append(round(angle, 2))

    # Normalize values
    normalized_depths = [round(d / 20000, 2) for d in defect_depths]
    normalized_angles = [round(a / (math.pi / 2), 2) for a in defect_angles]

    vector.append(finger_count + 1 if finger_count > 0 else 0)
    vector.extend(normalized_depths)
    vector.extend(normalized_angles)

    return vector


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    skinMask = cv2.inRange(ycrcb, lowerSkin, upperSkin)
    skinMask = cv2.GaussianBlur(skinMask, (5, 5), 0)

    contours, _ = cv2.findContours(skinMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        handCont = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(handCont)

        if 3000 < area < 30000:
            cv2.drawContours(frame, [handCont], -1, (0, 255, 0), 2)
            hull = cv2.convexHull(handCont)
            cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)

            hull_indices = cv2.convexHull(handCont, returnPoints=False)
            defects = cv2.convexityDefects(handCont, hull_indices)

            if defects is not None:
                finger_count = 0

                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = handCont[s][0]
                    end = handCont[e][0]
                    far = handCont[f][0]

                    a = np.linalg.norm(start - far)
                    b = np.linalg.norm(end - far)
                    c = np.linalg.norm(end - start)

                    if a == 0 or b == 0:
                        continue

                    angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b))

                    if d > 5000 and angle < math.pi / 2 and far[1] < frame.shape[0] * 0.8:
                        finger_count += 1
                        cv2.circle(frame, tuple(start), 6, (0, 0, 255), -1)
                        cv2.circle(frame, tuple(far), 5, (0, 255, 255), -1)

                fingers = finger_count + 1 if finger_count > 0 else 0
                cv2.putText(frame, f"Fingers: {fingers}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

            # 🔎 Extract the gesture vector
            gesture_vector = extract_gesture_vector(handCont, defects, frame.shape[0])
            print("Live vector:", gesture_vector)

    cv2.imshow("Hand Tracker", frame)
    cv2.imshow("Skin Mask", skinMask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
