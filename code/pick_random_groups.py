import numpy as np
with open('names.txt', 'r') as file:
    names = np.array([line.strip() for line in file])
print(names)
np.random.shuffle(names)
print(names)
groups = names.reshape(4,4)
print(groups)
for group in groups:
    print(group)

