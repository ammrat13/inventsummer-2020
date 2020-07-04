# Section 3: Introduction to Python.
# ==================================


# Section 3.1: Variables and Data Types
# -------------------------------------

# Type these lines into your python file so that you can work with these
# variables later on. 
num = 8.0
is_sunny = False
random_name = 'Rupert'

# Type print(random_name) in your python file, then run your program by
# clicking the green arrow on the top right corner of Visual Studio Code.
# You will see the output of your program in the terminal.  
print(random_name)

# Type print(square) and run your program to see the output! 
square = num * num
print(square)

# Add these lines to your program and run it, do you see "Bring an umbrella
# just in case" showing up in the terminal? (No)
if is_sunny:
    print("Let's go hiking")
else:
    print("Bring an umbrella just in case")

# Try changing the value of variable "is_sunny" from False to True, then run
# your program again. What do you see this time? ("Bring an ...")
is_sunny = False
if is_sunny:
    print("Let's go hiking")
else:
    print("Bring an umbrella just in case")

# Add this code block to your file and run your program. What's the output? Try
# modifying this code or coming up with your own if statements!
temperature = 25
if temperature > 25:
    print("Let's get some ice cream")
else:
    print("No ice cream I guess?")


# Section 3.2: Functions
# ----------------------

def my_first_function():
    print("Hi! You're trying something new!")
my_first_function()

def area_of_triangle(base, height):
    area = base * height * 0.5
    print("This triangle's area is", area)
area_of_triangle(35, 18)

def area_of_triangle(base, height):
    area = base * height * 0.5
    return area
return_value = area_of_triangle(35, 18)
print(return_value)


# Section 3.3: Lists and Indicies
# -------------------------------

# Outside of the function(s) you just made, create a list such as:
fruit_list = ['mango', 'watermelon', 'blueberry']

# Try these list operations in your editor to see how they work.
print(fruit_list[0])
fruit_list.append('cherry')
print(fruit_list)


# Section 3.4: Dictionaries
# -------------------------

little_women = {
    'author': "Louisa May Scott",
    'language': 'English',
    'year': 1868,
}
print(little_women['author'])
