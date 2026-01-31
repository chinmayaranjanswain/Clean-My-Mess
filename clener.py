import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Change this to your folder path (Example for Windows: "C:/Users/Name/Downloads")
TRACK_PATH = r"C:\Users\REC LIB7\Downloads"

EXTENSION_MAP = {
    # Images
    ".jpg": "Images", ".png": "Images", ".jpeg": "Images", ".gif": "Images",
    # Documents
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents", ".xlsx": "Spreadsheets",
    # Media
    ".mp4": "Videos", ".mp3": "Music",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives"
}

class MoverHandler(FileSystemEventHandler):
    # This function runs whenever a file is created or moved into the folder
   def on_modified(self, event):
        for filename in os.listdir(TRACK_PATH):
            file_path = os.path.join(TRACK_PATH, filename)
            
            if os.path.isdir(file_path) or filename.startswith('.'):
                continue
                
            extension = os.path.splitext(filename)[1].lower()
            
            if extension in EXTENSION_MAP:
                folder_name = EXTENSION_MAP[extension]
                dest_path = os.path.join(TRACK_PATH, folder_name)
                
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)

                # --- NEW SAFETY LOGIC ---
                try:
                    # Give the system 1 second to release the file lock
                    time.sleep(1) 
                    shutil.move(file_path, os.path.join(dest_path, filename))
                    print(f"Successfully organized: {filename} -> {folder_name}")
                except PermissionError:
                    # If file is busy, just skip it this time
                    print(f"File busy, skipping for now: {filename}")
                    continue
                except Exception as e:
                    print(f"Error moving {filename}: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, TRACK_PATH, recursive=False)
    
    print(f"Monitoring started on: {TRACK_PATH}")
    observer.start()
    
    try:
        while True:
            time.sleep(10) # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()