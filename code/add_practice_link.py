#!/usr/local/bin/python3
import json
import sys
"""
modify all summer experience notebooks to add a link to the practice notebook
in Google Colab

Usage:
    python add_practice_link.py Lessons/Lesson*.ipynb
"""
def main():
    for filename in sys.argv[1:]:
        add_link(filename)

"""
modify jupyter notebook json dict with new cell linking to the practice
:param notebook:
"""
def add_link(filename):
    with open(filename, 'r') as infile:
        notebook = json.load(infile)
    practice_name = f"Practice{filename.strip('Lessons/Lesson').split('.')[0]}"
    new_cell = {'cell_type': 'markdown', 'metadata': {'colab_type': 'text'}, 'source': [f"Click this link to go to the Practice notebook: [{practice_name}](https://colab.research.google.com/github/GWC-DCMB/SummerExperience/blob/master/Practices/{practice_name}.ipynb)"]}
    notebook['cells'].append(new_cell)
    with open(filename, 'w') as outfile:
        json.dump(notebook, outfile, indent=1)

main()