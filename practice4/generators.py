# Task 1


# This function is a generator that returns squares of numbers from 1 to N
def square_generator(N):
    # Loop from 1 to N (inclusive)
    for i in range(1, N + 1):
        # yield returns the value one by one (not all at once)
        yield i * i

# Call generator and print squares of numbers from 1 to 5
for square in square_generator(5):
    print("Task 1 result:", square)



# Task 2


# Generator that returns even numbers from 0 to A
def evenNumbers(A):
    # Loop from 0 to A (inclusive)
    for i in range(A + 1):
        # Check if number is even
        if i % 2 == 0:
            yield i  # Return even number

# Ask user to input a number
A = int(input("Enter number for Task 2: "))

# Convert each yielded number to string and join with comma
print("Task 2 result:", ",".join(str(num) for num in evenNumbers(A)))



# Task 3


# Generator that returns numbers divisible by BOTH 3 and 4
def divisible(C):
    # Loop from 0 to C (inclusive)
    for i in range(C + 1):
        # Check if number is divisible by 3 and 4
        # (which means divisible by 12)
        if i % 3 == 0 and i % 4 == 0:
            yield i

# Ask user for input
C = int(input("Enter number for Task 3: "))

# Print each number on new line
print("Task 3 result:")
for num in divisible(C):
    print(num)



# Task 4


# Generator that returns squares of numbers between a and b
def squares(a, b):
    # Loop from a to b (inclusive)
    for i in range(a, b + 1):
        yield i * i  # Return square of i

# Call generator for numbers from 2 to 6
print("Task 4 result:")
for value in squares(2, 6):
    print(value)


# Task 5

# Generator that counts down from f to 0
def decrease(f):
    # Continue while f is greater or equal to 0
    while f >= 0:
        yield f  # Return current value
        f -= 1   # Decrease f by 1

# Call generator starting from 6
print("Task 5 result:")
for h in decrease(6):
    print(h)