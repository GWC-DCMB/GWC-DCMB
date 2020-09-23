#!/usr/local/bin/python3
import os

def list_notebooks(dirname):
    return [file for file in sorted(os.listdir(dirname)) if "." in file and not file.startswith('.')]

def main():
    i = 1
    print('|   | Lesson Video | Lesson Notebook | Practice Notebook |')
    print('|---|---|---|---|')
    for lesson, practice in zip(list_notebooks("Lessons"), list_notebooks("Practices")):
            print(f"| {i} |   | [{' '.join(lesson.split('.')[0].split('_'))}](https://colab.research.google.com/github/GWC-DCMB/curriculum-notebooks/blob/master/Lessons/{lesson}) | [{' '.join(practice.split('.')[0].split('_'))}](https://colab.research.google.com/github/GWC-DCMB/curriculum-notebooks/blob/master/Practices/{practice}) |")
            i += 1

main()