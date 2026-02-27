# Task 1


# Import datetime (for date & time)
# and timedelta (for time difference calculations)
from datetime import datetime, timedelta

# Get the current date and time
current_date = datetime.now()

# Subtract 5 days from the current date
# timedelta(days=5) creates a 5-day time difference
new_date = current_date - timedelta(days=5)

# Print the new date (5 days ago)
print("Task 1 result:", new_date)


# Task 2


# Import date class separately (only date, no time)
from datetime import date

# Get today's date
today = date.today()

# Calculate yesterday (1 day before today)
yesterday = today - timedelta(days=1)

# Calculate tomorrow (1 day after today)
tomorrow = today + timedelta(days=1)

# Print all dates
print("Task 2 results:")
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)



# Task 3


# Get current date and time (includes microseconds)
now = datetime.now()

# Remove microseconds using replace()
# It keeps all values but sets microsecond = 0
without_microseconds = now.replace(microsecond=0)

# Print cleaned datetime
print("Task 3 result:", without_microseconds)



# Task 4


# Ask user to input first date
# Format must be: YYYY-MM-DD HH:MM:SS
date1_str = input("Enter first date (YYYY-MM-DD HH:MM:SS): ")

# Ask user to input second date
date2_str = input("Enter second date (YYYY-MM-DD HH:MM:SS): ")

# Convert strings to datetime objects
# strptime() parses string according to format
date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

# Calculate difference between two dates
# Subtraction gives timedelta object
# total_seconds() converts it into seconds
# abs() ensures the result is positive
difference = abs((date2 - date1).total_seconds())

# Print difference in seconds as integer
print("Task 4 result (seconds difference):", int(difference))