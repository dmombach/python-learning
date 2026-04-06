from app.services import bootstrap_contacts
from app.contacts import remove_contact, search_contact, list_contacts
from app.utils import safe_int, safe_get_contact

# region Examples, Basic Info

# print("Hello Dan, welcome to Python!")

# >>> Variables
# name = "Dan"
# age = 45

# >>> Types
# • int
# • float
# • str
# • bool
# • list
# • dict
# • tuple


# >>> Functions
# def greet(name):
# return f"Hello {name}"


# print(greet("Super Dan"))

# >>> Conditionals
# if age > 18:
# print("Adult")
# else:
# print("Minor")

# >>> Loops
# for i in range(5):
# print(i)

# >>> Modules
# import math

# >>> Packages (pip)
# pip install requests

# >>> Virtual environments
# You already created one.

# >>> File I/O
# with open("data.txt") as f:
#     print(f.read())

# >>> Classes (Python’s simple OOP)
# class Person:
#     def __init__(self, name):
#         self.name = name

# EXCEPTIONS - Here’s what you’ll use 90% of the time:
# Exception         When it happens
# ValueError	    Wrong value (e.g., int("abc"))
# TypeError	        Wrong type (e.g., 3 + "a")
# KeyError	        Missing dict key
# IndexError	    List index out of range
# FileNotFoundError	Opening a missing file
# ZeroDivisionError	Division by zero
# AttributeError	Accessing missing attribute

# endregion

# Add some contacts
bootstrap_contacts()

# List contacts
for c in list_contacts():
    print(f"{c['name']} - {c['phone']}")


# Remove contact
name = "Alice"
if remove_contact(name) == True:
    print(f"{name} removed.")
else:
    print(f"{name} not found.")


# Search contact
name = "Dan"
result = search_contact(name)
if result:
    print(f"{result['name']} - {result['phone']}")
else:
    print(f"{name} not found.")

name = "Alice"
result = search_contact(name)
if result:
    print(f"{result['name']} - {result['phone']}")
else:
    print(f"{name} not found.")

# Safe search
result = safe_get_contact("Dan", search_contact)
print(f"From Safe Search: {result}")

# Exception trials
try:
    number = int("abc")
except ValueError:
    print("Invalid number!")

try:
    result = search_contact("Bob")
    print(result["phone"])
except TypeError:
    print("Contact not found.")

# utils experimentations
print(safe_int("123"))
print(safe_int("abc"))
print(safe_int(None, -1))
