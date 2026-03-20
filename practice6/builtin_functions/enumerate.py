names = ["Ali", "John", "Sara"]
scores = [90, 85, 88]

# enumerate() → gives index + value
for i, name in enumerate(names):
    print(i, name)

# zip() → combines lists into pairs
for name, score in zip(names, scores):
    print(name, score)