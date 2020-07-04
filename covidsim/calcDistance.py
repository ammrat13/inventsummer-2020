# Section 4: The Problem of Distance
# ==================================


# Section 4.1: Introduction to Python Classes
# -------------------------------------------

# Let's do this in code:
# Let's create a class ourselves to see how all of this works.
# In the "calcDistance.py" file that you created, start creating a Person class:
class Person:

    # Section 4.1.1: Attributes
    isMortal = True
    def __init__(self, n, a):
        self.name = n
        self.age = a

    # Section 4.1.3: Methods
    def greeting(self):
        print("Hi! My name is " + self.name)
    def start_conversation(self):
        self.greeting()
        print("What's your name?")


# Section 4.1.2: Constructor
# Run your program to try it out! You can run your program by clicking the
# green arrow on the top right corner of Visual Studio Code. You will see the
# output of your program in the terminal.
person1 = Person('Alex', 18)
print(person1.name)

# Section 4.1.3: Methods
# Try creating two person objects and call greeting() on each of them!
person1 = Person('Alex', 18)
person2 = Person('Jess', 15)
person1.greeting()
person2.greeting()
# Try calling start_conversation() on person objects you've created!
person1.start_conversation()
person2.start_conversation()


# Section 4.2: Distance Calculation Using Classes
# -----------------------------------------------

# In section 2.1, we decided that a person's location and health status are
# crucial information. To capture those, we can add them as instance variables
# in Person class.
class Person:

    isMortal = True

    # Update your __init__ function to take in variables for location and health
    # status.
    def __init__(self, n, a, x_coord, y_coord, h):
        self.name = n
        self.age = a
        self.x = x_coord
        self.y = y_coord
        self.health = h

    # If we want to put this function inside the class instead of outside, we
    # could turn this function into an instance method like this:
    def calc_distance(self, p2):
        dx = self.x - p2.x
        dy = self.y - p2.y
        distance = (dx**2 + dy**2)**0.5
        return distance

# Now think of how you'll calculate the distance between them.
# Try writing the code to implement the distance formula in python. 
# You might need to do power operation, which is done by ** in python. in math
# becomes 2**3 in python.
person1 = Person('Alex', 18, 1, 1, 'healthy')
person2 = Person('Jess', 15, 13, 20, 'recovered')
dx = person1.x - person2.x
dy = person1.y - person2.y
distance = (dx**2 + dy**2)**0.5
print("Alex and Jess are", distance, "miles apart from each other")

# So we can put these lines of code inside a function, and use 2 person objects
# as inputs:
def calc_distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = (dx**2 + dy**2)**0.5
    return distance
print(calc_distance(person1, person2))
print(person1.calc_distance(person2))


# Section 4.3: Calculate Distance for the Entire Population
# ---------------------------------------------------------

import random

# Section 4.3.1: Loop Exercise
# For the purpose of testing how to calculate distance, let's give everyone a
# placeholder name, age, and health status. We will only give random self.x and
# self.y.
pop_size = 3000
population = []
for i in range(pop_size):
    p = Person('', 0, random.randint(0, 100), random.randint(0, 100), '')
    population.append(p)
# To address this issue, let's create a list called distance to store the
# distance between every pair of people.
distance = []
for a in population:
    a_dist = []
    for b in population:
        dist = calc_distance(a,b)
        a_dist.append(dist)
    distance.append(a_dist)

# Section 4.3.2: Performance
# To measure the performance, let's time the code.
import timeit
def func(pop_size):
    population = []
    for i in range(pop_size):
        p = Person('', 0, random.randint(0, 100), random.randint(0, 100), '')
        population.append(p)
    distance = []
    for a in population:
        a_dist = []
        for b in population:
            dist = calc_distance(a,b)
            a_dist.append(dist)
        distance.append(a_dist)
# You can paste this line of code into your file and make several copies of it.
# In each copy, choose a different population size to pass into func(). 
# Now, run your code and see how much time it takes to calculate distance using
# the current method!
print(timeit.timeit(lambda:func(3),number=1))
print(timeit.timeit(lambda:func(30),number=1))
print(timeit.timeit(lambda:func(300),number=1))
print(timeit.timeit(lambda:func(3000),number=1))
