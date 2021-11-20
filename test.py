import numpy as np

my_data = [[2, 1, 5], [2, 3, 5]]
mystring = ""
for entry in my_data:
    for input in entry:
        mystring += str(input)
    mystring += "\n"
del my_data[1]
images = np.array([i + 1 for i in range(20)])
images = np.delete(images, 2)

print(images)
