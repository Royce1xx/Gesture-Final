import os
import shutil
import zipfile

# === CONFIGURATION ===
ZIP_PATH = r"C:\Users\genui\Downloads\Nohands.zip"  # Use raw string (r"") to avoid \ errors
EXTRACT_DIR = "temp_extracted"
DEST_DIR = "flat_folder"
VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# === EXTRACT ZIP ===
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

# === SETUP DESTINATION FOLDER ===
os.makedirs(DEST_DIR, exist_ok=True)

# === WALK AND COLLECT IMAGES ===
count = 0
for root, dirs, files in os.walk(EXTRACT_DIR):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in VALID_EXTENSIONS:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(DEST_DIR, f"{count}_{file}")
            shutil.copy2(src_path, dst_path)
            count += 1

print(f"✅ Moved {count} image(s) to '{DEST_DIR}'")
