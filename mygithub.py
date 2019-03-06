#!/usr/bin/env python3
import sys
import os
import git

# так мы указываем где лежат сторонние библиотеки
sys.path.append('{}/venv/lib64/python3.6/site-packages'.format(os.getcwd()))


LOCAL_REPO = "mytestproject"
LOCAL_WIKI = "wiki_dir"
BEGIN_SSH = "git@github.com:{}"


class Gengit:

    def __init__(self, ssh_url, branch='master'):
        self.url = ssh_url
        self.local_repo = LOCAL_REPO
        self.local_wiki = LOCAL_WIKI
        self.branch = branch
        self.repo = None

    def download_git(self):
        self.repo = git.Repo.clone_from(self.url, self.local_repo)
        self.repo.git.checkout(self.branch)

    def download_git_wiki(self):
        git_url = BEGIN_SSH.format(self.url[19:])
        self.repo = git.Repo.clone_from(git_url, self.local_wiki)

    def add(self, filename):
        self.repo.index.add([filename])
        self.repo.index.commit('add report')

    def push(self):
        self.repo.git.push('origin', self.branch)

