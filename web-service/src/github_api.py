#!./venv/bin/python3.6
import sys
import os
import git
import requests


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

API_GITHUB = "https://api.github.com/repos/{}/{}/pulls/{}/comments"
# GET /repos/:owner/:repo/pulls/:pull_number/comments
POSITION = "original_position"
USER = "user"
LOGIN = "login"
BODY = "body"
DIFF_HUNK = "diff_hunk"



class Gengit:

    def __init__(self, ssh_url="", branch=STANDART_BRANCH):
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

    def get_response(self, url):
        params = {"sort": "updated"}
        response = requests.get(url, params=params)
        return response

    def comporator(self, object):
        return object[POSITION]

    def new_hunk(self, string):
        s = string.split('\n')
        length = len(s) - 1
        new_str = []
        while s[length][0] == "+":
            new_str.append(s[length][1:] + "\n")
            length -= 1
        return ''.join(new_str)

    def create_comments_for_word(self, my_json):
        mylist = []
        my_json = sorted(my_json, key=self.comporator)
        for comment in my_json:
            mylist.append([comment[POSITION], comment[USER][LOGIN], comment[BODY],
                           self.new_hunk(comment[DIFF_HUNK])])
        return mylist

    class comment:
        def __init__(self, id):
            self.body_comments = []
            self.id = id
            self.body_code = ""

    # 0 - id | 1 - login | 2 - comment | 3 - body
    def optimization_comments(self, comments):
        total_comments = []
        for element in comments:
            if len(total_comments) > 0 and element[0] == total_comments[len(total_comments) - 1].id:
                total_comments[len(total_comments) - 1].body_comments.append([element[1], element[2]])
                continue
            my_comment = self.comment(element[0])
            my_comment.body_comments.append([element[1], element[2]])
            my_comment.body_code = element[3]
            total_comments.append(my_comment)
        return total_comments

    def get_comments(self, company, name_of_repo, pull_requests):
        comments = []
        for number_of_pr in pull_requests:
            url = API_GITHUB.format(company, name_of_repo, number_of_pr)
            response = self.get_response(url)
            comments += self.create_comments_for_word(response.json())
        return self.optimization_comments(comments)
