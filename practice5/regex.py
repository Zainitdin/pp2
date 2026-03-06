# Python Regular Expressions Practice
# This file contains solutions for 10 RegEx exercises.
# Each task demonstrates how regular expressions can be used
# to identify, manipulate, or transform text patterns.

import re


# -----------------------------------------------------
# 1. Match a string that has 'a' followed by zero or more 'b'
# -----------------------------------------------------
# Regex explanation:
# a  -> string starts with 'a'
# b* -> zero or more occurrences of 'b'
pattern1 = r"ab*"

strings1 = ["a", "ab", "abb", "ac"]

print("Task 1:")
for s in strings1:
    if re.fullmatch(pattern1, s):
        print(f"{s} -> Match")
print()


# -----------------------------------------------------
# 2. Match a string that has 'a' followed by two to three 'b'
# -----------------------------------------------------
# Regex explanation:
# b{2,3} -> between 2 and 3 occurrences of 'b'
pattern2 = r"ab{2,3}"

strings2 = ["abb", "abbb", "abbbb", "ab"]

print("Task 2:")
for s in strings2:
    if re.fullmatch(pattern2, s):
        print(f"{s} -> Match")
print()


# -----------------------------------------------------
# 3. Find sequences of lowercase letters joined with underscore
# -----------------------------------------------------
# Example pattern: hello_world
# Regex explanation:
# [a-z]+ -> one or more lowercase letters
# _      -> underscore
# [a-z]+ -> one or more lowercase letters again
text3 = "hello_world test_value Hello_World"

pattern3 = r"[a-z]+_[a-z]+"

matches3 = re.findall(pattern3, text3)

print("Task 3:")
print(matches3)
print()


# -----------------------------------------------------
# 4. Find sequences of one uppercase letter followed by lowercase letters
# -----------------------------------------------------
# Example: London, Paris
# Regex explanation:
# [A-Z]  -> one uppercase letter
# [a-z]+ -> one or more lowercase letters
text4 = "London paris NewYork Tokyo Berlin"

pattern4 = r"[A-Z][a-z]+"

matches4 = re.findall(pattern4, text4)

print("Task 4:")
print(matches4)
print()


# -----------------------------------------------------
# 5. Match a string that starts with 'a' and ends with 'b'
# -----------------------------------------------------
# Regex explanation:
# a  -> string begins with 'a'
# .* -> any characters (0 or more)
# b  -> ends with 'b'
pattern5 = r"a.*b"

strings5 = ["ab", "axxb", "a123b", "ac"]

print("Task 5:")
for s in strings5:
    if re.fullmatch(pattern5, s):
        print(f"{s} -> Match")
print()


# -----------------------------------------------------
# 6. Replace spaces, commas, or dots with colon
# -----------------------------------------------------
# Regex explanation:
# [ ,\.] -> character class matching
# space OR comma OR dot
text6 = "Hello, world. Python is great."

result6 = re.sub(r"[ ,\.]", ":", text6)

print("Task 6:")
print(result6)
print()


# -----------------------------------------------------
# 7. Convert snake_case to camelCase
# -----------------------------------------------------
# Example:
# hello_world -> helloWorld
#
# Regex explanation:
# _([a-z]) -> underscore followed by a letter
# The lambda function converts the letter to uppercase
text7 = "hello_world_python"

result7 = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text7)

print("Task 7:")
print(result7)
print()


# -----------------------------------------------------
# 8. Split string at uppercase letters
# -----------------------------------------------------
# Example:
# HelloWorldPython -> ['Hello', 'World', 'Python']
#
# Regex explanation:
# (?=[A-Z]) -> positive lookahead
# Splits before every uppercase letter
text8 = "HelloWorldPython"

result8 = re.split(r"(?=[A-Z])", text8)

print("Task 8:")
print(result8)
print()


# -----------------------------------------------------
# 9. Insert spaces between words starting with capital letters
# -----------------------------------------------------
# Example:
# HelloWorldPython -> Hello World Python
#
# Regex explanation:
# ([A-Z]) -> matches uppercase letters
# \1 -> inserts the matched letter again with a space before it
text9 = "HelloWorldPython"

result9 = re.sub(r"([A-Z])", r" \1", text9).strip()

print("Task 9:")
print(result9)
print()


# -----------------------------------------------------
# 10. Convert camelCase to snake_case
# -----------------------------------------------------
# Example:
# helloWorldPython -> hello_world_python
#
# Regex explanation:
# ([A-Z]) -> find uppercase letters
# Replace with '_' + letter
# Then convert the whole string to lowercase
text10 = "helloWorldPython"

result10 = re.sub(r"([A-Z])", r"_\1", text10).lower()

print("Task 10:")
print(result10)
print()