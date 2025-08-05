import cv2
import os

# Create directories if they don't exist
os.makedirs("dataset1/hand", exist_ok=True)
os.makedirs("dataset1/no_hand", exist_ok=True)

cap = cv2.VideoCapture(0)
cv2.namedWindow("Collect Data", cv2.WINDOW_NORMAL)

hand_count = len(os.listdir("dataset1/hand"))
nohand_count = len(os.listdir("dataset1/no_hand"))

print("📸 Press 'H' to save hand image")
print("🌫️ Press 'N' to save no-hand image")
print("❌ Press 'Q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    display_frame = frame.copy()

    cv2.putText(display_frame, "Press H - Hand | N - No Hand | Q - Quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Collect Data", display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('h'):
        filepath = f"dataset1/hand/hand_{hand_count}.jpg"
        cv2.imwrite(filepath, frame)
        hand_count += 1
        print(f"✅ Saved HAND image #{hand_count} -> {filepath}")

    elif key == ord('n'):
        filepath = f"dataset1/no_hand/no_hand_{nohand_count}.jpg"
        cv2.imwrite(filepath, frame)
        nohand_count += 1
        print(f"✅ Saved NO-HAND image #{nohand_count} -> {filepath}")

    elif key == ord('q'):
        print("🛑 Quitting image collection.")
        break

cap.release()
cv2.destroyAllWindows()
