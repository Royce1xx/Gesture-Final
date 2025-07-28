import cv2
import numpy as np
import math

# Create resizable display window
cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)

# Open webcam
cap = cv2.VideoCapture(0)

# Define lower and upper skin color thresholds in YCrCb
lowerSkin = np.array([0, 133, 77], dtype=np.uint8)
upperSkin = np.array([255, 173, 127], dtype=np.uint8)

# Extract a simplified gesture vector from hand contour and convexity defects
def extract_gesture_vector(contour, defects, frame_height):
    vector = []
    defect_depths = []
    defect_angles = []
    finger_count = 0

    # Process all defects (valleys between fingers)
    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = contour[s][0]
            end = contour[e][0]
            far = contour[f][0]

            # Distances for triangle sides
            a = np.linalg.norm(start - far)
            b = np.linalg.norm(end - far)
            c = np.linalg.norm(end - start)

            # Skip invalid triangles
            if a == 0 or b == 0:
                continue

            # Calculate angle using cosine rule
            angle = math.acos((a**2 + b**2 - c**2) / (2 * a * b))

            # Only count tight valleys above wrist height
            if d > 5000 and angle < math.pi / 2 and far[1] < frame_height * 0.8:
                finger_count += 1
                defect_depths.append(int(d))
                defect_angles.append(round(angle, 2))

    # Normalize depths and angles
    normalized_depths = [round(d / 20000, 2) for d in defect_depths]
    normalized_angles = [round(a / (math.pi / 2), 2) for a in defect_angles]

    # Build vector: [fingers, depth1, depth2, ..., angle1, angle2, ...]
    vector.append(finger_count + 1 if finger_count > 0 else 0)
    vector.extend(normalized_depths)
    vector.extend(normalized_angles)

    return vector

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert frame to YCrCb and apply skin mask
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    skinMask = cv2.inRange(ycrcb, lowerSkin, upperSkin)
    skinMask = cv2.GaussianBlur(skinMask, (5, 5), 0)

    # Find all contours in the skin mask
    contours, _ = cv2.findContours(skinMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If any contours found
    if contours:
        # Choose largest contour (assumed to be hand)
        handCont = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(handCont)

        # Ignore contours too small or too large
        if 3000 < area < 30000:
            # Draw hand contour
            cv2.drawContours(frame, [handCont], -1, (0, 255, 0), 2)

            # Draw convex hull
            hull = cv2.convexHull(handCont)
            cv2.drawContours(frame, [hull], -1, (255, 0, 0), 2)

            # Get convex hull indices and defects
            hull_indices = cv2.convexHull(handCont, returnPoints=False)
            defects = cv2.convexityDefects(handCont, hull_indices)

            # Count fingers based on defects
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

                    # Draw circles for valid valleys
                    if d > 5000 and angle < math.pi / 2 and far[1] < frame.shape[0] * 0.8:
                        finger_count += 1
                        cv2.circle(frame, tuple(start), 6, (0, 0, 255), -1)
                        cv2.circle(frame, tuple(far), 5, (0, 255, 255), -1)

                # Final finger count = defects + 1
                fingers = finger_count + 1 if finger_count > 0 else 0

                # Draw finger count text
                cv2.putText(frame, f"Fingers: {fingers}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

            # Calculate gesture vector and print it
            gesture_vector = extract_gesture_vector(handCont, defects, frame.shape[0])
            print("Live vector:", gesture_vector)

    # Show both frames
    cv2.imshow("Hand Tracker", frame)
    cv2.imshow("Skin Mask", skinMask)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
