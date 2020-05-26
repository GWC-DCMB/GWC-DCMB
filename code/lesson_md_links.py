#!/usr/local/bin/python3
import os
for file in sorted(os.listdir("Lessons")):
    if "." in file and not file.startswith('.'):
        print(f"- [{' '.join(file.split('.')[0].split('_'))}](https://colab.research.google.com/github/GWC-DCMB/SummerExperience/blob/master/Lessons/{file})")
