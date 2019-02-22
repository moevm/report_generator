#!/usr/bin/env python3
#import gitPython
import sys,os
sys.path.append(os.getcwd()+'/venv/lib64/python3.6/site-packages')
import git
import sys

class gengit():

    def __init__(self,ssh_url,branch='master'):
        self.url = ssh_url
        self.local_repo = "mytestproject"
        self.local_wiki = "wiki_dir"
        self.branch = branch
        self.repo = None

    def downloadgit(self):
        self.repo = git.Repo.clone_from(self.url, self.local_repo)
        if self.repo is None:
            print('repo is None')
            sys.exit(1)
        self.repo.git.checkout(self.branch)

    def downloadgitwiki(self):
        git_url = 'git@github.com:' + self.url[19:]
#self.url[0:-3] + 'wiki.git'
        self.repo = git.Repo.clone_from(git_url, self.local_wiki)
        if self.repo is None:
            print('wiki is None')
            sys.exit(1)

    def add(self, filename):
        self.repo.index.add([filename])
        self.repo.index.commit('add report')

    def push(self):
        #self.repo.git.pull('origin', self.branch)
        self.repo.git.push('origin', self.branch)
    pass


