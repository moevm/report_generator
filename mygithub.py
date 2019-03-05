#!/usr/bin/env python3
import sys
import os
import git

# так мы указываем где лежат сторонние библиотеки
sys.path.append('{}/venv/lib64/python3.6/site-packages'.format(os.getcwd()))


LOCAL_REPO = "mytestproject"
LOCAL_WIKI = "wiki_dir"
BEGIN_SSH = "git@github.com:{}"

class Gengit():

    def __init__(self, ssh_url, branch='master'):
        self.url = ssh_url
        self.local_repo = LOCAL_REPO
        self.local_wiki = LOCAL_WIKI
        self.branch = branch
        self.repo = None

    def downloadgit(self):
        self.repo = git.Repo.clone_from(self.url, self.local_repo)
        if self.repo is None:
            print('repo is None')
        self.repo.git.checkout(self.branch)

    def downloadgitwiki(self):
        git_url = BEGIN_SSH.format(self.url[19:])
        self.repo = git.Repo.clone_from(git_url, self.local_wiki)
        if self.repo is None:
            print('wiki is None')

    def add(self, filename):
        self.repo.index.add([filename])
        self.repo.index.commit('add report')

    def push(self):
        self.repo.git.push('origin', self.branch)
