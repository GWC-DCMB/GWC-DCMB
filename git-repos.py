""" Collect repository information from GitHub and generate a markdown table.

Usage:
    git-repos.py -h | --help
    git-repos.py --username=<your_username> [--token=<path_to_token>] [--include_private]

Options:
    -h --help                       Display this help message.
    -u --username=<your_username>   Your GitHub username.
    -t --token=<path_to_token>      Path to a text file containing your GitHub access toekn.
    --include_private               Whether to include private repos. [default: False]
"""
import base64
import collections
import datetime
from docopt import docopt
from getpass import getpass
from github import Github
import json
import os
import plotly
import yaml

PROJECTS_HEADER = '## Repositories\n'

def main(args):
    """
    Collects repositories the user owns or has contributed to
    and updates the Projects table in README.md
    """
    for dir in ('figures',):
        if not os.path.exists(dir):
            os.mkdir(dir)

    print("Logging into GitHub...")
    if args['--token']:
        with open(args['--token'], 'r') as token_file:
            token = token_file.readline().strip()
        github = Github(token)
    else:
        password = getpass("Enter your GitHub password: ")
        github = Github(args['--username'], password)

    projects = Repos(github, args['--username'], include_private=args['--include_private'])

    print("Updating the Projects table...")
    with open('README.md', 'r') as file:  # collect everything except the old projects table
        head = [file.readline()]
        line = file.readline()
        while line != PROJECTS_HEADER:
            head.append(line)
            line = file.readline()
        assert line == PROJECTS_HEADER
        line = file.readline()
        while not line.startswith("## "):  # TODO: don't loop indefinitely if there's no heading afer Projects
            line = file.readline()  # skip stuff under Projects subheading
        tail = ['\n'+line]
        for line in file:
            tail.append(line)

    with open('README.md', 'w') as file:
        file.writelines(head)
        file.writelines(projects.markdown_table)
        file.writelines(tail)
    print("Done!")


def count_jupyter_bytes(gh_repo):
    """ Count bytes of code in Jupyter code blocks
    :param gh_repo: github repo from pygithub
    :return: bytes of code in code blocks
    """
    bytes_count = 0
    contents = gh_repo.get_contents("")
    while len(contents) > 1:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(gh_repo.get_contents(file_content.path))
        elif file_content.name.endswith('.ipynb'):
            #print(file_content, file_content.type, file_content.size, file_content.name)
            if file_content.size < 1e+6:  # TODO: need to use Git Data API to handle large Jupyter notebooks
                jsondict = json.loads(base64.b64decode(file_content.content).decode('utf-8').strip("'"))
                for cell in jsondict['cells']:
                    if cell['cell_type'] == 'code':
                        for line in cell['source']:
                            bytes_count += len(line.encode('utf-8'))
    return bytes_count


class Repos:
    """ Store information about a user's github repositories & generate a markdown table """
    status_options = ['Current', "Stale", "Archive"]

    def __init__(self, github, username, include_private=False):
        """
        :param github: a github object from pygithub
        :param include_private: whether to include private repositories
        """
        user = github.get_user(username)
        language_data = {'all_bytes': LangStat("My languages by bytes of code on GitHub", 'bytes of code', 'all_bytes'),
                         'all_repos': LangStat('My languages by presence in GitHub repositories', '# of repos', 'all_repos'),
                         'top_bytes': LangStat("Top repo languages by bytes of code on GitHub", 'bytes of code', 'top_bytes'),
                         'top_repos': LangStat("Top languages by GitHub repositories", '# of repos', 'top_repos')}
        self.repos = {status: [] for status in self.__class__.status_options}
        # iterate over all repos this user has read access to
        prev_repo_owner = ''
        print("Collecting repos:")
        for gh_repo in user.get_repos():
            if prev_repo_owner != gh_repo.owner.login:
                prev_repo_owner = gh_repo.owner.login
                print(f"\t{prev_repo_owner}")
            # only count repositories the user owns or contributes to
            is_owner = gh_repo.owner == user
            is_contributor = user in gh_repo.get_contributors()
            if (is_owner or is_contributor):
                print(f"\t\t{gh_repo.name}")
                languages = gh_repo.get_languages()  # excludes vendored languages from the repo's .gitattributes
                for lang in ("HTML", "CSS"):  # drop these because they're usually not hand-written by me
                    languages.pop(lang, None)
                if languages:
                    print(f"\t\t\t{sorted(languages.keys(), key = lambda k: languages[k], reverse = True)}")
                    for lang, bytes_count in languages.items():  # aggregate bytes counts for all languages
                        if lang == "Jupyter Notebook":
                            bytes_count = count_jupyter_bytes(gh_repo)
                        language_data['all_bytes'].add(lang, bytes_count)
                    language_data['all_repos'].update(languages.keys())
                    top_language = max(languages, key = lambda k: languages[k])
                    language_data['top_repos'].add(top_language, 1)
                    language_data['top_bytes'].add(top_language, count_jupyter_bytes(gh_repo) if lang == "Jupyter Notebook" else languages[top_language])
                # respect privacy preference
                if (include_private or not gh_repo.private):
                    repo = Repo(gh_repo)
                    self.repos[repo.status].append(repo)

    @property
    def markdown_table(self):
        """
        :return: a list containing strings in markdown table format
        """
        table = [PROJECTS_HEADER]

        table.append(f"\n| Repository | Description | Language(s) |\n|---|---|---|\n")
        for status in self.repos:
            for repo in self.repos[status]:
                table.append(repo.markdown)

        return table


class Repo:
    """ Store info about a github repository """
    six_months = datetime.timedelta(days=182)

    def __init__(self, repo):
        """ Store minimal info about a github repository
        :param repo: a github repository object from pygithub
        """
        self.owner = f"[{repo.owner.login}]({repo.owner.html_url})"
        self.name = f"[{repo.name}]({repo.html_url})"
        self.description = repo.description
        self.languages = ', '.join(repo.get_languages())
        if repo.archived:
            status = "Archive"
        elif (datetime.datetime.now() - repo.updated_at) > self.__class__.six_months:
            status = "Stale"
        else:
            status = "Current"
        assert status in Repos.status_options
        self.status = status
        self.last_modified = repo.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return f"| {self.name} | {self.description} | {self.languages} |\n"


class Gist:
    def __init__(self, gist):
        """ Store minimal info about a github Gist
        :param gist: a github gist object from pygithub
        """
        self.name = gist.description
        self.owner = f"[{gist.owner.login}]({gist.owner.html_url})"
        self.description = f"[{gist.description}]({gist.html_url})"
        self.last_modified = gist.updated_at.strftime("%Y-%m-%d")

    @property
    def markdown(self):
        return f"| {self.description} |\n"


class LangStat:
    def __init__(self, description, count_type, name):
        self.description = description
        self.count_type = count_type
        self.filename = f'figures/language_{name}'
        self.counter = collections.Counter()

    def __repr__(self):
        return f"{self.__class__}({self.__dict__})"

    def add(self, key, value):
        self.counter[key] += value

    def update(self, iterable):
        self.counter.update(iterable)

    def make_plot(self, num_repos=None):
        tuples = self.counter.most_common(num_repos)
        x = [lang[0] for lang in tuples]
        y = [lang[1] for lang in tuples]
        figure = plotly.graph_objs.Figure(data=[plotly.graph_objs.Bar(x=x, y=y, text=y, textposition='auto')],
                                          layout=plotly.graph_objs.Layout(title=self.description,
                                                                          xaxis=dict(tickangle=45),
                                                                          yaxis=dict(title=self.count_type,
                                                                                     automargin=True)))
        plotly.io.write_image(figure, f"{self.filename}.svg" if not num_repos else f"{self.filename}_n{num_repos}.svg")


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
