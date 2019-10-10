# How to Contribute

We use the [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) workflow to make our lives easier. This means all new lessons, practices, and edits should be made in separate branches -- not the `master` branch.
View the issues in our repositories to see what we need. If an issue isn't assigned to anyone, we would welcome your contribution!

If you have questions or run into problems at any point, contact [Kelly](mailto:sovacool@umich.edu).

## Table of Contents

- [Setup](#setup)
- [Creating or editing](#creating-or-editing)
- [Reviewing](#reviewing)
- [Notes](#notes)

## Setup

### Git

If you haven't already:

1. Configure git on your local machine.

    Use the same email that is associated with your GitHub account.
    ```
    git config --global user.name "Firstname Lastname"
    git config --global user.email "you@email.com"
    ```

1. Clone the repo you want to contribute to.
    ```
    git clone repo-url
    ```
    
    e.g. if you want to contribute to our `ClubCurriculum`, the `repo-url` would be `https://github.com/GWC-DCMB/ClubCurriculum.git`.

If you need a refresher, Software Carpentry has a lesson on [Version Control with Git](http://swcarpentry.github.io/git-novice/).

### Dependencies

We teach with [Google Colab](https://colab.research.google.com), which has all of our dependencies already installed. 
However, we recommend editing the notebooks by running [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) on your local machine ([why?](#jupyterlab)). 
The minimum required dependencies are listed in the [environment file](environment.yml). 
You're welcome to use your package manager of choice (Kelly's recommendation: [conda](https://docs.conda.io/en/latest/miniconda.html)).

## Creating or editing

1. Move to the repo directory on your computer (cloned above during [git setup](#git).)

    ```
    cd repo-name
    ```

1. Create a new branch for your feature.
    
    Give it a short, descriptive name.
    ```
    git checkout -b new-branch-name
    ```
    Alternatively, if you don't have write access to the repository, you'll need to [fork the repo](https://help.github.com/en/articles/fork-a-repo) instead and work on your fork.

1. Make your edits.
    ```
    jupyter lab notebook-name.ipynb
    ```
    Be sure to save them from Jupyter!
    If you're creating a new lesson or practice, it's easiest to edit the lesson key, 
    then copy the key to the lesson folder and remove any blanks that you want to be filled in during the live coding demo.
    Don't forget to run all cells in Key files and clear output from regular Lessons & Practices ([instructions](#cell-output)).

1. Commit & push your changes.
    ```
    git add notebook-name.ipynb
    git commit -m "Edit lesson XX"
    ```
    See commit message guidelines [here](#commit-messages).
    
    If you're pushing your branch for the first time, you'll have to set the upstream:
    ```
    git push --set-upstream origin new-branch-name
    ```

    Otherwise, just push like usual:
    ```
    git push origin new-branch-name
    ```

    If you forget the branch name, you can list existing branches using the command:
    ```
    git branch --list
    ```

1. Open a pull request [[example](https://github.com/GWC-DCMB/ClubCurriculum/pull/21)].
    1. Open the repo page in your web browser (e.g. [the ClubCurriculum repo](https://github.com/GWC-DCMB/ClubCurriculum)).
    1. If you want to see what the modifications look like before opening a pull request, you can go to the document you modified and change the branch to the left of the file name. 
    1. Go to the pull requests tab and click `new pull request`.
    1. Select your branch name to compare to master. If you forked the repo instead of making a branch, select "compare across forks" instead.
    1. Create the pull request.
    1. Assign a reviewer.
    The reviewer will then take a look at the changes, make any edits as needed, and merge the branch into master.

## Reviewing

1. Make sure your local copy of the repo is up-to-date.
    ```
    git pull
    ```
1. Checkout the branch corresponding to the pull request you're reviewing.
    ```
    git checkout branch-name
    ```
1. Review and edit the contents.
    ```
    jupyter lab notebook-name.ipynb
    ```
    Make sure the [cell outputs](#cell-output) are correct.
    
1. Commit & push changes if needed.
    ```
    git add notebook-name.ipynb
    git commit -m "Revise lesson XX"
    git push
    ```

1. Merge the pull request when you're happy with it.

    Either press the `merge` button on Github in your web browser,
    or do it from the command line:
    ```
    git checkout master
    git merge branch-name master
    ```
    In the merge commit message, reference any [issues](https://github.com/GWC-DCMB/ClubCurriculum/issues) (our To-Do list) that the pull request resolves so the issue is closed automatically. 
    For example, the [commit](https://github.com/GWC-DCMB/ClubCurriculum/commit/e871017fc77fe2023f2488d3c18ae4baaee5b03f) message I wrote when adding this file was `Add contributing instructions (Resolves #11)`.
    
    If no more work will be done on that branch, you can delete it on Github to reduce clutter.

## Notes

### Commit messages

We recommend this [style guide](https://chris.beams.io/posts/git-commit/) for writing good commit messages.
The highlights:
- Capitalize the first word of the message.
- The first word should be a verb in the imperative tense.
- Keep the message short but descriptive of the changes.

### File paths

If you need to read in a dataset, Pandas can read https links to raw github files. Example:

```
path = 'https://raw.githubusercontent.com/GWC-DCMB/SummerExperience/master/'
tips = pd.read_csv(path + 'SampleData/tips.csv')
```
    
Don't use local filepaths (e.g. `pd.read_csv('../SampleData/tips.csv')`), because we live-code in Google Colab.

If you come across legacy references to mounting Google Drive, please remove them. We previously used this Colab feature, but have decided to use links to raw github files instead (see above).

### Cell output

**Keys**:
Every Key (filename starts with `KEY_`) should show the output of all cells.  Make sure Keys work by running all cells in JupyterLab by clicking `Run` > `Run All Cells`. 

**Lessons & Practices**:
The output cells of every Lesson and Practice notebook should be empty. To remove the output cells from a notebook, click `Edit` > `Clear All Outputs`.

### JupyterLab

**TLDR**: When editing notebooks, be sure to use JupyterLab on your local machine. If you open a notebook with Google Colab, please don't commit the changes.

Jupyter notebooks are text files in [JSON format](https://www.json.org/), which can be conveniently parsed as Python dictionaries. JupyterLab formats them nicely with tab indentation & individual fields on different lines (i.e. [pretty-print](https://docs.python.org/3.4/library/pprint.html)), like this:

```
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "KSChitqaVpii"
   },
   "source": [
    "# Subsetting Pandas DataFrames I\n",
    "\n",
    "You now know how to read external datasets into `pandas`. Let's put those skills to use and read in the `tips` dataset again:"
   ]
  },
...
```

However, when you open a Jupyter notebook with Google Colab, it squishes all of the content onto one line, like this:
```
{ "cells": [  {   "cell_type": "markdown",   "metadata": {    "colab_type": "text",    "id": "KSChitqaVpii"   },   "source": [    "# Subsetting Pandas DataFrames I\n",    "\n",    "You now know how to read external datasets into `pandas`. Let's put those skills to use and read in the `tips` dataset again:"   ]  },
```

This makes it difficult to compare & merge Jupyter notebooks written in JupyterLab vs Colab via `git diff`.
To keep our notebooks easy to compare & merge, we strongly prefer JupyterLab for editing.
