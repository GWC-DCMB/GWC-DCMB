"""
A one-use script to update notebook numbers after inserting a new Lesson 18 (Dictionaries)
"""
import os
import re

old_numbers = set(range(19,27))
subdirs = ["Lessons/", "Lessons/_Keys/", "Practices/", "Practices/_Keys/"]

input_filenames = [f"{subdir}{fn}" for subdir in subdirs for fn in os.listdir(subdir) if fn.endswith(".ipynb") and not fn.startswith(".") and int(re.search("\d\d", fn)[0]) in old_numbers]
output_filenames = list()
for fn in input_filenames:
    old_number = re.search("\d\d", fn)[0]
    new_number = str(int(old_number) + 1)
    if len(new_number) < 2:
        new_number = '0' + new_number
    output_filenames.append(re.sub(old_number, new_number, fn))

assert len(input_filenames) == len(output_filenames)

for old, new in zip(input_filenames, output_filenames):
    print(old, new)
    os.rename(old, new)

