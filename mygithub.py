#!./venv/bin/python3.6
import sys
import os
import git
import requests
import json


LOCAL_REPO = "mytestproject"
LOCAL_WIKI = "wiki_dir"
BEGIN_SSH = "git@github.com:{}"
SIZE_OF_SSH_ADDRESS = 19
COMMIT_MESSAGE = 'add report'
ORIGIN = 'origin'
STANDART_BRANCH = 'master'

PARAM = "updated"
API_GITHUB_COMMENTS = "https://api.github.com/repos/OSLL/report_generator/pulls/comments"
TIME_FILE = "file_for_api_git.txt"

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
            return False
        self.repo.git.checkout(self.branch)

    def download_git_wiki(self):
        git_url = BEGIN_SSH.format(self.url[SIZE_OF_SSH_ADDRESS:])
        try:
            self.repo = git.Repo.clone_from(git_url, self.local_wiki)
        except Exception:
            return False

    def add(self, filename):
        self.repo.index.add([filename])
        self.repo.index.commit(COMMIT_MESSAGE)

    def push(self):
        self.repo.git.push(ORIGIN, self.branch)

    @staticmethod
    def get_comments():
        response = requests.get(API_GITHUB_COMMENTS,params=PARAM)
        with open(TIME_FILE, 'w') as file:
            file.write(response.text)
        with open(TIME_FILE, 'r') as file:            
            js = json.load(file)
        i = 0
        list_comments = []
        while i < len(js):
            list_comments.append([js[i]["original_position"],js[i]["created_at"],js[i]["user"]["login"],js[i]["body"]])
            i += 1
        list_comments.sort()
        return list_comments
