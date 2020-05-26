#!/usr/local/bin/python3
import os
import shutil

def main():
    with open('GWC-DCMB/curriculum.tsv', 'r') as infile:
        curriculum = [line.strip('\n').split('\t') for line in infile]
    for new_dir in ["Lessons", "Practices"]:
        os.makedirs(os.path.dirname(f"summerExperience/{new_dir}/_Keys/pdf"),
                    exist_ok=True)
    for club_file, summer_file in curriculum:
        if summer_file:
            shutil.copy(f"clubCurriculum/{club_file}",
                        f"summerExperience/{summer_file}")

main()