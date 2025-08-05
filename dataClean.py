import os
import cv2
from tqdm import tqdm

# ==== CONFIGURATION ====
INPUT_FOLDER = "preclean_folder"
OUTPUT_FOLDER = "dataset/cleannohands"
IMAGE_SIZE = (128, 128)
VALID_EXTS = ['.jpg', '.jpeg', '.png']
MIN_IMAGE_DIM = 50

# ==== SETUP ====
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
existing_files = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith(tuple(VALID_EXTS))]
image_count = len(existing_files)  # Start after last image in output

# ==== VALIDATION FUNCTION ====
def is_valid_image(img):
    if img is None:
        return False
    if img.shape[0] < MIN_IMAGE_DIM or img.shape[1] < MIN_IMAGE_DIM:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if cv2.Laplacian(gray, cv2.CV_64F).var() < 15:
        return False
    return True

# ==== MAIN LOOP ====
for filename in tqdm(os.listdir(INPUT_FOLDER)):
    ext = os.path.splitext(filename)[-1].lower()
    if ext not in VALID_EXTS:
        continue

    try:
        path = os.path.join(INPUT_FOLDER, filename)
        img = cv2.imread(path)

        if is_valid_image(img):
            resized = cv2.resize(img, IMAGE_SIZE)
            new_name = f"hand_{image_count:05d}.jpg"
            cv2.imwrite(os.path.join(OUTPUT_FOLDER, new_name), resized)
            image_count += 1
    except Exception:
        continue

print(f"\n✅ Done! Cleaned and saved {image_count} total images to '{OUTPUT_FOLDER}'.")
