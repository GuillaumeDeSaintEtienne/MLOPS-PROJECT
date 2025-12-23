import kagglehub
import shutil
import os
from pathlib import Path

# --- Configuration ---
dataset_name = "parisrohan/credit-score-classification"
destination_path = Path("src/data/datasets") 

# --- 1. Download Dataset ---
print(f"Downloading {dataset_name}...")
cache_path = kagglehub.dataset_download(dataset_name)
print(f"Dataset downloaded to cache at: {cache_path}")

# --- 2. Create Target Folder ---
print(f"Ensuring destination directory exists: {destination_path}")
destination_path.mkdir(parents=True, exist_ok=True)

# --- 3. Move CSV Files ---
print("Moving files...")
files_moved = 0

for file_name in os.listdir(cache_path):
    if file_name.endswith(".csv"):
        source = Path(cache_path) / file_name
        dest = destination_path / file_name
        
        if dest.exists():
            print(f"Skipping {file_name} (already exists in target).")
        else:
            shutil.move(str(source), str(dest))
            print(f"Moved: {file_name}")
            files_moved += 1

if files_moved == 0:
    print("No new CSV files were moved (folder might already contain the data).")
else:
    print(f"Successfully moved {files_moved} files.")