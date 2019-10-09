#!/bin/bash

function update() {
    source ~/.bash_profile
    conda activate git-repos
    python git-repos.py --token .token --username GWC-DCMB
}

function commit() {
    git add .
    git commit -m "Auto-update repos"
    git push
}

if update; then
    commit
else
    echo "* Update failed! *"
fi
