# Open file in read mode ("r")
with open("sample.txt", "r") as f:
    # Read entire content at once
    print("Full content:")
    print(f.read())

# Open again to demonstrate line-by-line reading
with open("sample.txt", "r") as f:
    print("Line by line:")
    for line in f:
        # strip() removes newline characters
        print(line.strip())