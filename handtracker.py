import cv2
import numpy as np
import math
import json
import os

cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cap = cv2.VideoCapture(0)

# Combined YCrCb and HSV thresholds
lower_YCrCb = np.array([0, 133, 77], dtype=np.uint8)
upper_YCrCb = np.array([255, 173, 127], dtype=np.uint8)

lower_HSV = np.array([0, 30, 60], dtype=np.uint8)
upper_HSV = np.array([20, 150, 255], dtype=np.uint8)

GESTURE_FILE = "gestures.json"

# Load or initialize gesture data
if os.path.exists(GESTURE_FILE):
    with open(GESTURE_FILE, "r") as f:
        gesture_db = json.load(f)
else:
    gesture_db = {}

def save_gesture_data():
    with open(GESTURE_FILE, "w") as f:
        json.dump(gesture_db, f)

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
            if d > 3000 and angle < math.pi / 2 and far[1] < frame_height * 0.9:
                finger_count += 1
                defect_depths.append(int(d))
                defect_angles.append(round(angle, 2))

    normalized_depths = [round(d / 20000, 2) for d in defect_depths]
    normalized_angles = [round(a / (math.pi / 2), 2) for a in defect_angles]
    vector.append(finger_count + 1 if finger_count > 0 else 0)
    vector.extend(normalized_depths)
    vector.extend(normalized_angles)
    return vector

def match_gesture(live_vec, target_vecs, threshold=0.5):
    for vec in target_vecs:
        max_len = max(len(live_vec), len(vec))
        live_padded = live_vec + [0] * (max_len - len(live_vec))
        target_padded = vec + [0] * (max_len - len(vec))
        dist = np.linalg.norm(np.array(live_padded) - np.array(target_padded))
        if dist < threshold:
            return True
    return False

def get_combined_skin_mask(frame):
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(ycrcb, lower_YCrCb, upper_YCrCb)
    mask2 = cv2.inRange(hsv, lower_HSV, upper_HSV)
    combined_mask = cv2.bitwise_and(mask1, mask2)
    combined_mask = cv2.GaussianBlur(combined_mask, (5, 5), 0)
    return combined_mask

recording = False
current_label = ""
sample_buffer = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    mask = get_combined_skin_mask(frame)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        hand_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(hand_contour)
        x, y, w, h = cv2.boundingRect(hand_contour)
        aspect_ratio = w / float(h)

        if 3000 < area < 40000 and 0.5 < aspect_ratio < 1.5:
            cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)

            hull = cv2.convexHull(hand_contour)
            hull_indices = cv2.convexHull(hand_contour, returnPoints=False)
            defects = cv2.convexityDefects(hand_contour, hull_indices)

            gesture_vector = extract_gesture_vector(hand_contour, defects, frame.shape[0])
            print("Live vector:", gesture_vector)

            if recording:
                sample_buffer.append(gesture_vector)
                cv2.putText(frame, f"Recording {current_label}: {len(sample_buffer)}/30", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                if len(sample_buffer) >= 30:
                    gesture_db[current_label] = sample_buffer.copy()
                    save_gesture_data()
                    print(f"Saved gesture: {current_label}")
                    sample_buffer.clear()
                    recording = False
            else:
                for label, vectors in gesture_db.items():
                    if match_gesture(gesture_vector, vectors):
                        cv2.putText(frame, f"Matched: {label}", (10, 130),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        print(f"Matched gesture: {label}")
                        break
        else:
            cv2.putText(frame, "❌ Rejected - Not hand shape", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("Hand Tracker", frame)
    cv2.imshow("Skin Mask", mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c') and not recording:
        current_label = input("Enter gesture label: ")
        sample_buffer = []
        recording = True
        print(f"Started recording gesture: {current_label}")

cap.release()
cv2.destroyAllWindows()
