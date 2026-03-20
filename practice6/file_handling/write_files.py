from pathlib import Path

# Create a file path object (cross-platform safe)
file_path = Path("sample.txt")

# Open file in write mode ("w") → creates file or overwrites it
with open(file_path, "w") as f:
    # Write lines into the file
    f.write("Hello, this is the first line\n")
    f.write("Second line\n")

print("File created and written.")