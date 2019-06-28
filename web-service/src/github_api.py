#!./venv/bin/python3.6
import git


LOCAL_REPO = "repo_for_report"
LOCAL_WIKI = "wiki_dir"
BEGIN_SSH = "git@github.com:{}"
SIZE_OF_SSH_ADDRESS = 19
COMMIT_MESSAGE = 'add report'
ORIGIN = 'origin'
STANDART_BRANCH = 'master'
ERROR_WIKI = "Wrong link to wiki!"
ERROR_REPO = "Wrong link to repository!"
ERROR_BRANCH = "Branch doesnt exist!"


class Gengit:

    def __init__(self, ssh_url, branch=STANDART_BRANCH):
        self.url = ssh_url
        self.local_repo = LOCAL_REPO
        self.local_wiki = LOCAL_WIKI
        self.branch = branch
        self.repo = None

    def download_git(self):
        try:
            self.repo = git.Repo.clone_from(self.url, self.local_repo)
        except git.GitCommandError as e:
            print(ERROR_REPO)
            print(e.command)
            return False
        try:
            self.repo.git.checkout(self.branch)
        except git.GitCommandError as e:
            print(ERROR_BRANCH)
            print(e.command)
            return False

    def download_git_wiki(self):
        git_url = BEGIN_SSH.format(self.url[SIZE_OF_SSH_ADDRESS:])
        try:
            self.repo = git.Repo.clone_from(git_url, self.local_wiki)
        except git.GitCommandError as e:
            print(e.command)
            print(ERROR_WIKI)
            return False

    def add(self, filename):
        try:
            self.repo.index.add([filename])
            self.repo.index.commit(COMMIT_MESSAGE)
        except git.GitCommandError as e:
            print(e.command)

    def push(self):
        try:
            self.repo.git.push(ORIGIN, self.branch)
        except git.GitCommandError as e:
            print(e.command)
