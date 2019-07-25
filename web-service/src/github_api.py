#!./venv/bin/python3.6
import sys
import os
import git
import requests
from word import ABS_PATH
from github import Github


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
ERROR_PUSH = 'this file has been in repository yet'
NEW_FILENAME = '{}{}.pdf'
LEN_PDF = 4
GEN_PATH_REPORT = '{}/{}'

TOKEN = '4d7baf087e8e9536c68fbebe4a51ba4304f4cfa1'
HEADER = {'Authorization': 'token {}'.format(TOKEN)}
INVITE_PATH = 'user/repository_invitations'
API = 'https://api.github.com/{}'
INVITE_URL = 'url'


class Gengit:

    def __init__(self, ssh_url, branch=STANDART_BRANCH):
        check_invites()
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

    def push(self, filename=''):
        path = GEN_PATH_REPORT.format(LOCAL_REPO, filename)
        my_github = Github(TOKEN)
        content = ''
        with open(path, 'rb') as file:
            content = file.read()
        repo = my_github.get_repo(self.url[15:-4])
        is_sent = False
        number_try = 0
        while not is_sent:
            try:
                repo.create_file(filename, COMMIT_MESSAGE, content, branch=self.branch)
                is_sent = True
            except Exception:
                print(ERROR_PUSH)
                filename = NEW_FILENAME.format(filename[:-LEN_PDF - number_try], number_try)
                number_try += 1
        return filename


def get_requests(path, full_path=False):
    if not full_path:
        return requests.get(API.format(path), headers=HEADER).json()
    else:
        return requests.patch(path, headers=HEADER)


def accept_invite(invite):
    get_requests(invite, full_path=True)


def get_invites():
    return get_requests(INVITE_PATH)


def check_invites():
    for invite in get_invites():
        print(invite[INVITE_URL])
        accept_invite(invite[INVITE_URL])

