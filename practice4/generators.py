#Task 1

def square_generator(N):
    for i in range(1, N + 1):
        yield i * i

for square in square_generator(5):
    print(square)

#Task 2

def evenNumbers(A):
    for i in range(A+1):
        if i%2==0:
            yield i

A=int(input())
print(",".join(str(num) for num in evenNumbers(A)))

#Task 3

def divisible(C):
    for i in range(C+1):
        if i % 3 == 0 and i % 4==0:
            yield i

C=int(input())
for num in divisible(C):
    print(num)

#Task 4

def squares(a, b):
    for i in range(a, b+1):
        yield i*i

for value in squares(2,6):
    print(value)

#Task 5
def decrease(f):
    while f>=0:
        yield f
        f-=1
for h in decrease(6):
    print(h)