# Task 1 – Convert Degrees to Radians


# Import math module (contains mathematical constants and functions)
import math

# Ask user to input angle in degrees
degree = float(input("Input degree: "))

# Convert degrees to radians
# Formula: radians = degrees × (π / 180)
radian = degree * (math.pi / 180)

# Print result
print("Output radian:", radian)


# Task 2 – Area of a Trapezoid
import math

# Height and two bases of trapezoid
height = 5
base1 = 5
base2 = 6

# Formula for trapezoid area:
# Area = (base1 + base2) × height / 2
area_trapezoid = (base1 + base2) * height / 2

# Print result
print("Area of trapezoid:", area_trapezoid)


# Task 3 – Area of a Regular Polygon

import math
# Ask user for number of sides
n = int(input("Input number of sides: "))

# Ask user for length of one side
s = float(input("Input the length of a side: "))

# Formula for regular polygon area:
# Area = (n × s²) / (4 × tan(π / n))
area_polygon = (n * s ** 2) / (4 * math.tan(math.pi / n))

# Print integer part of area
print("The area of the polygon is:", int(area_polygon))

# Task 4 – Area of a Parallelogram

import math
# Base and height values
base = 5
height = 6

# Area formula:
# Area = base × height
# math.prod() multiplies elements of list together
area_parallelogram = math.prod([base, height])

# Print result as float
print("Area of parallelogram:", float(area_parallelogram))