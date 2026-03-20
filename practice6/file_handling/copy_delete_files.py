import shutil
import os

# Copy file → creates a duplicate (backup)
shutil.copy("sample.txt", "backup.txt")
print("File copied.")

# Check if file exists before deleting (safe delete)
if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("File deleted.")
else:
    print("File does not exist.")