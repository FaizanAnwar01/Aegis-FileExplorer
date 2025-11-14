
# ---------------- file_operations.py ----------------
import os
import shutil
import zipfile
import datetime

BACKUP_DIR = "backup"
LOG_FILE = os.path.join("logs", "file_manager.log")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def log_action(action, filepath):
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.datetime.now().strftime("[%d-%b %H:%M:%S]")
        log.write(f"{timestamp} {action}: {filepath}\n")

def parse_extension(ext_str):
    ext = ext_str.strip()
    return ext if ext.startswith(".") else f".{ext}"

def move_files_by_extension(source, dest, extension, progress_callback, status_callback):
    matched_files = [f for f in os.listdir(source) if f.endswith(extension)]
    total = len(matched_files)

    if not matched_files:
        raise FileNotFoundError("No matching files to move.")

    os.makedirs(dest, exist_ok=True)

    for i, file in enumerate(matched_files):
        src_path = os.path.join(source, file)
        dest_path = os.path.join(dest, file)
        backup_file(src_path)
        shutil.move(src_path, dest_path)
        progress_callback(i + 1, total)
        status_callback(f"Moved: {file}")
        log_action("Moved", dest_path)

def delete_files_by_extension(source, extension, progress_callback, status_callback):
    matched_files = [f for f in os.listdir(source) if f.endswith(extension)]
    total = len(matched_files)

    if not matched_files:
        raise FileNotFoundError("No matching files to delete.")

    for i, file in enumerate(matched_files):
        file_path = os.path.join(source, file)
        backup_file(file_path)
        os.remove(file_path)
        progress_callback(i + 1, total)
        status_callback(f"Deleted: {file}")
        log_action("Deleted", file_path)

def list_files_recursive(source):
    file_list = []
    for root, dirs, files in os.walk(source):
        for f in files:
            full_path = os.path.join(root, f)
            file_list.append(full_path)
    return file_list

def list_files_with_extension(source, extension):
    file_list = []
    for root, dirs, files in os.walk(source):
        for f in files:
            if f.endswith(extension):
                file_list.append(os.path.join(root, f))
    return file_list

def search_files_by_name(source, pattern):
    result = []
    for root, dirs, files in os.walk(source):
        for f in files:
            if pattern.lower() in f.lower():
                full_path = os.path.join(root, f)
                result.append(full_path)
    return result

def backup_file(filepath):
    zip_name = os.path.join(BACKUP_DIR, "backup.zip")
    with zipfile.ZipFile(zip_name, "a") as zipf:
        arcname = os.path.relpath(filepath, start=os.path.dirname(filepath))
        zipf.write(filepath, arcname)
        log_action("Backed up", filepath)

def undo_last_action():
    zip_path = os.path.join(BACKUP_DIR, "backup.zip")
    if not os.path.exists(zip_path):
        return "No backup available."

    extract_path = os.path.join(BACKUP_DIR, "undo_restore")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_path)

    return f"Undo successful. Files restored to '{extract_path}' folder."


