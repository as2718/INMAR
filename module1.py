import os
import hashlib
import json
from datetime import datetime
from variables import PROCESSED_FILES_LOG, BAD_OUTPUT_PATH, OUTPUT_PATH
import shutil


# Function to get all files in the source directory

def get_all_files_in_directory(directory):
    # List all files and directories
    all_items = os.listdir(directory)

    # Filter out only the files
    files = [f for f in all_items if os.path.isfile(os.path.join(directory, f))]

    return files


# Load the log file
def load_processed_files():
    if os.path.exists(PROCESSED_FILES_LOG):
        with open(PROCESSED_FILES_LOG, 'r') as f:
            return json.load(f)
    return {}


# Save the log file
def save_processed_files(log):
    with open(PROCESSED_FILES_LOG, 'w') as f:
        json.dump(log, f)


# Generate a unique hash for a file (to identify unique files)
def generate_sha256_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:  # Make sure the file is opened in binary mode
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


# Check if the file is new (hasn't been processed yet)
def is_new_file(file_path):
    processed_files = load_processed_files()
    file_hash = generate_sha256_hash(file_path)

    # Check if the file hash has already been processed today
    if file_hash in processed_files:
        print(f"File '{file_path}' has already been processed .")
        return False
    return True


# Check if the file is empty
def is_non_empty_file(file_path):
    if os.path.getsize(file_path) > 0:
        print(os.path.getsize(file_path))
        return True
    else:
        print(f"File '{file_path}' is empty. Skipping.")
        return False


# Check if the file extension is .csv
def is_csv_file(file_path):
    if file_path.lower().endswith('.csv'):
        return True
    else:
        print(f"File '{file_path}' is not a .csv file. Skipping.")
        return False


# Process the file
def process_file(file_path):
    if is_new_file(file_path) and is_csv_file(file_path) and is_non_empty_file(file_path):
        # Simulate file processing
        print(f"Processing file: {file_path}")

        # Update log with the file hash and current date
        processed_files = load_processed_files()
        file_hash = generate_sha256_hash(file_path)
        processed_files[file_hash] = datetime.now().strftime("%Y-%m-%d")
        shutil.move(file_path, OUTPUT_PATH)
        save_processed_files(processed_files)
        print(f"File: {file_path} Validated Successfully\n")

    else:
        print(f"Skipping file: {file_path}")
        shutil.move(file_path, BAD_OUTPUT_PATH)
        print(f"File: {file_path} Validation unsuccessful , moved to {BAD_OUTPUT_PATH}\n")
