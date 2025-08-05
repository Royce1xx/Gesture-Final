import os
import shutil
import zipfile

# === CONFIGURATION ===
ZIP_PATH = r"C:\Users\genui\Downloads\Nohands4.zip"
EXTRACT_DIR = "temp_extracted"
DEST_DIR = "flat_folder2"
VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# === EXTRACT ZIP ===
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

# === SETUP DESTINATION FOLDER ===
os.makedirs(DEST_DIR, exist_ok=True)

# === GET EXISTING FILE COUNT ===
existing_files = os.listdir(DEST_DIR)
count = len(existing_files)

# === WALK AND COLLECT IMAGES ===
for root, dirs, files in os.walk(EXTRACT_DIR):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in VALID_EXTENSIONS:
            # Generate a unique filename like hand_00001.jpg
            new_name = f"hand_{count:05}{ext}"
            while new_name in existing_files:
                count += 1
                new_name = f"hand_{count:05}{ext}"

            src_path = os.path.join(root, file)
            dst_path = os.path.join(DEST_DIR, new_name)
            shutil.copy2(src_path, dst_path)
            existing_files.append(new_name)
            count += 1

print(f"✅ Finished copying. Total images now: {len(existing_files)}")
