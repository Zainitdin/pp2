from functools import reduce

nums = [1, 2, 3, 4, 5]

# map() → apply function to each element (square numbers)
squares = list(map(lambda x: x**2, nums))
print("Squares:", squares)

# filter() → keep only elements that match condition (even numbers)
evens = list(filter(lambda x: x % 2 == 0, nums))
print("Evens:", evens)

# reduce() → combine elements into one value (sum)
total = reduce(lambda x, y: x + y, nums)
print("Sum:", total)