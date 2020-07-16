# Section 5: How to Calculate Distance Faster
# ===========================================


# Section 5.1: Put Everyone's Location in One Matrix?
# ---------------------------------------------------

# Let's create a new file called "npCalcDistance.py". In this file, we aim to
# achieve the same functionality as "calcDistance.py", but with better
# performance.
import numpy as np

# Now, pick a population size and try to create the random location data using
# numpy. These initial locations will be the starting point of our simulation.
pop_size = 3000
xs = np.random.randint(low=0, high=100, size=(pop_size,))
ys = np.random.randint(low=0, high=100, size=(pop_size,))

# Once you make your array and store it in a variable, try
# print(*variable_name*) and run your code multiple times to see what location
# values are generated. Values in the array should be different every time.
print(xs)
print(ys)


# Section 5.2: Intro to NumPy
# ---------------------------

# Section 5.2.1: Numpy's Powers: Single Instruction Multiple Data
a = np.array(range(1, 10)).reshape((3,3))
b = np.array(range(1, 10)).reshape((3,3))
c = a * b
print(c)

# Section 5.2.2: Creating Empty Arrays
# Running this code will make (10, 18) appear on your screen. 
a = np.zeros((10,18))
print(a.shape)
# A 2D array can have just 1 row or just 1 column, as in the following example:
column_array = np.zeros((5,1))
print(column_array.shape)
row_array = np.zeros((1,5))
print(row_array.shape)

# Section 5.2.5: Square Root and Power
a = np.array(range(1,10)).reshape((3,3))
b = np.array(range(1,4))
print(np.sqrt(a))
print(a**0.5)
print(a**b)


# Section 5.3: Write a Function that Calculates Distance
# ------------------------------------------------------
dxs = xs - xs.reshape((pop_size,1))
dys = ys - ys.reshape((pop_size,1))
dists = (dxs**2 + dys**2)**0.5
print(dists)


# Section 5.4: Performance
# ------------------------

import timeit

# Now run the code and see how long it takes for numpy to calculate every
# pairwise distance within the population.
def calc_all_dists(pop_size):
    xs = np.random.randint(low=0, high=100, size=(pop_size,))
    ys = np.random.randint(low=0, high=100, size=(pop_size,))
    dxs = xs - xs.reshape((pop_size,1))
    dys = ys - ys.reshape((pop_size,1))
    dists = (dxs**2 + dys**2)**0.5
    return dists

# Now run the code and see how long it takes for numpy to calculate every
# pairwise distance within the population.
print(timeit.timeit(lambda: calc_all_dists(3), number=1))
print(timeit.timeit(lambda: calc_all_dists(30), number=1))
print(timeit.timeit(lambda: calc_all_dists(300), number=1))
print(timeit.timeit(lambda: calc_all_dists(3000), number=1))
