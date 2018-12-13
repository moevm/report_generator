#!/usr/bin/env python3
#import gitPython
import git
import requests
import sys
class gengit():
    def __init__(self,login,password,url,branch='master'):
        self.url = url
        self.local_repo = "mytestproject"
        self.test_branch = branch
        self.login = login
        self.branch = branch
        self.password = password
        self.repo = None

    def downloadgit(self, url):
        git_url = url[0:8] + self.login + ':' + self.password + '@' + url[8:]
        self.repo = git.Repo.clone_from(git_url, self.local_repo)
        if self.repo is None:
            print('repo is None')
            sys.exit(1)
        self.repo.git.checkout(self.branch)


    def checkwiki(self):
        path = 'https://raw.githubusercontent.com'+self.url[18:-4]+'/'+self.branch+'/'+'settings.json'
        wiki = requests.get(path)#https://raw.githubusercontent.com/light5551/test_gen/test_branch/test.c
        #print(wiki)
        if wiki.status_code is not 200:
            print('There is no wiki in repository')
            sys.exit(0)
        return wiki.text

    def add(self, filename):
        #print(filename)
        self.repo.index.add([filename])
        self.repo.index.commit('add report')

    def push(self):
        #self.repo.git.pull('origin', self.branch)
        self.repo.git.push('origin', self.branch)
    pass
pass

