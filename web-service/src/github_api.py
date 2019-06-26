#!./venv/bin/python3.6
import sys
import os
import git
from word import ABS_PATH


LOCAL_REPO = ABS_PATH.format("repo_for_report")
LOCAL_WIKI = ABS_PATH.format("wiki_dir")
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
        except Exception:
            print(ERROR_REPO)
            return False
        try:
            self.repo.git.checkout(self.branch)
        except Exception:
            print(ERROR_BRANCH)
            return False

    def download_git_wiki(self):
        git_url = BEGIN_SSH.format(self.url[SIZE_OF_SSH_ADDRESS:])
        try:
            self.repo = git.Repo.clone_from(git_url, self.local_wiki)
        except Exception:
            print(ERROR_WIKI)
            return False

    def add(self, filename):
        self.repo.index.add([filename])
        self.repo.index.commit(COMMIT_MESSAGE)

    def push(self):
        self.repo.git.push(ORIGIN, self.branch)
