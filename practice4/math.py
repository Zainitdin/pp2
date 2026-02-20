#Task 1

import math

degree = float(input("Input degree: "))


radian = degree * (math.pi / 180)

print("Output radian:", radian)

#Task 2

import math

height = 5
base1 = 5
base2 = 6

area = (base1 + base2) * height / 2

print("Area of trapezoid:", area)

#Task 3

import math


n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s ** 2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", int(area))

#Task 4

import math

base = 5
height = 6

area = math.prod([base, height]) 

print("Area of parallelogram:", float(area))