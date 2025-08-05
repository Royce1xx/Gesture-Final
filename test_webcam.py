import cv2
import numpy as np
import tensorflow as tf

# === Load the trained model ===
model = tf.keras.models.load_model("cnn1_hand_vs_nohand_final.h5")

# === Config ===
IMAGE_SIZE = 128
LABELS = ["No Hand", "Hand"]

# === Open webcam ===
cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Detection", cv2.WINDOW_NORMAL)

print("📷 Press 'Q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and preprocess the frame
    frame = cv2.flip(frame, 1)
    resized = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
    normalized = resized / 255.0
    input_img = np.expand_dims(normalized, axis=0)  # shape: (1, 128, 128, 3)

    # === Predict ===
    prediction = model.predict(input_img, verbose=0)[0][0]
    label = LABELS[1] if prediction > 0.5 else LABELS[0]
    confidence = prediction if prediction > 0.5 else 1 - prediction

    # === Display prediction ===
    color = (0, 255, 0) if label == "Hand" else (0, 0, 255)
    cv2.putText(frame, f"{label} ({confidence*100:.2f}%)", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
