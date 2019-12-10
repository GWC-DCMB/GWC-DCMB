"""
Remove 'colab' item from 'metadata' and enforce JupyterLab's indentation style.
"""
import json
import os

subdirs = ["Lessons/", "Lessons/_Keys/", "Practices/", "Practices/_Keys/"]
filenames = [f"{subdir}{fn}" for subdir in subdirs for fn in os.listdir(subdir) if fn.endswith(".ipynb") and not fn.startswith(".")]

for fn in filenames:
    with open(fn, 'r') as file:
        notebook = json.load(file)
    if 'colab' in notebook['metadata']:
        notebook['metadata'].pop('colab')
        with open(fn, 'w') as file:
            json.dump(notebook, file, indent=1)