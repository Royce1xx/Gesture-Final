import os
import shutil
import random
import string

# === CONFIG ===
SOURCE_DIR = "flat_folder2"
DEST_DIR = "preclean_folder"
VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# === CREATE DESTINATION IF NOT EXISTS ===
os.makedirs(DEST_DIR, exist_ok=True)

# === RANDOM SUFFIX GENERATOR ===
def random_suffix(length=2):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# === MOVE FILES WITH MODIFIED NAMES ===
moved = 0
for file in os.listdir(SOURCE_DIR):
    ext = os.path.splitext(file)[1].lower()
    if ext in VALID_EXTENSIONS:
        base = os.path.splitext(file)[0]
        suffix = random_suffix()
        new_name = f"{base}_{suffix}{ext}"
        dest_path = os.path.join(DEST_DIR, new_name)

        # Just in case — add more randomness if needed
        while os.path.exists(dest_path):
            suffix = random_suffix(3)
            new_name = f"{base}_{suffix}{ext}"
            dest_path = os.path.join(DEST_DIR, new_name)

        shutil.move(os.path.join(SOURCE_DIR, file), dest_path)
        moved += 1

print(f"✅ Moved {moved} files with unique filenames to '{DEST_DIR}'")
