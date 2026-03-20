import os

# Create nested directories (no error if already exists)
os.makedirs("test_dir/sub_dir", exist_ok=True)

# List all files and folders in current directory
print("Directory contents:", os.listdir("."))

# Get current working directory
print("Current dir:", os.getcwd())