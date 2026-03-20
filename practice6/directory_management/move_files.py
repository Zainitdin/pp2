import shutil
import os

# Create destination folder if it doesn't exist
os.makedirs("dest", exist_ok=True)

# Move file to another directory
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "dest/sample.txt")
    print("File moved.")
else:
    print("File not found.")