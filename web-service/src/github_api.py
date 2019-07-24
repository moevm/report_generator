#!./venv/bin/python3.6
import subprocess
import git
import requests
import time
from app import ABS_PATH

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

API_GITHUB = "https://api.github.com/repos/{}/{}/pulls/{}/comments"
POSITION = "original_position"
USER = "user"
LOGIN = "login"
BODY = "body"
COMMIT = "original_commit_id"
DIFF_HUNK = "diff_hunk"
FILENAME_DIFF = "diff_file.txt"
FILENAME_LOG = "log_file.txt"
LOG_SH = "./do_git_log.sh {}"
DIFF_SH = "./do_git_diff.sh {} {} {}"
PLUS = "+"
MINUS = "-"


class Gengit:

    def __init__(self, ssh_url="", branch=STANDART_BRANCH):
        self.url = ssh_url
        self.local_repo = LOCAL_REPO
        self.local_wiki = LOCAL_WIKI
        self.branch = branch
        if branch is '':
            self.branch = 'master'
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

    def new_hunk(self, diff_string):
        lines_of_diff = diff_string.split('\n')
        length = len(lines_of_diff) - 1
        new_str = []
        while lines_of_diff[length][0] == PLUS:
            new_str.append("{}{}".format(lines_of_diff[length][1:], '\n'))
            length -= 1
        return ''.join(new_str)

    def create_comments_for_word(self, my_json):
        mylist = []
        my_json = sorted(my_json, key=self.comporator)
        for comment in my_json:
            mylist.append([comment[POSITION], comment[USER][LOGIN], comment[BODY],
                           self.new_hunk(comment[DIFF_HUNK]), comment[COMMIT][0:7]])
        return mylist

    class comment:
        def __init__(self, id):
            self.body_comments = []
            self.id = id
            self.body_code = ""
            self.commit = ""
            self.diff = ""

    def optimization_comments(self, comments):
        total_comments = []
        for element in comments:
            if len(total_comments) > 0 and element[0] == total_comments[len(total_comments) - 1].id:
                total_comments[len(total_comments) - 1].body_comments.append([element[1], element[2]])
                continue
            my_comment = self.comment(element[0])
            my_comment.body_comments.append([element[1], element[2]])
            my_comment.body_code = element[3]
            my_comment.commit = element[4]
            total_comments.append(my_comment)
        return total_comments

    def get_comments(self, company, name_of_repo, pull_requests):
        comments = []
        for number_of_pr in pull_requests:
            url = API_GITHUB.format(company, name_of_repo, number_of_pr)
            response = self.get_response(url)
            comments += self.create_comments_for_word(response.json())
        main_comments = self.optimization_comments(comments)
        return self.add_diff(main_comments, main_comments[0].commit)

    def add_diff(self, comments, original_commit):
        self.create_log(self.local_repo)
        end_commit = self.find_next_commit(original_commit)
        self.create_dif(self.local_repo, self.branch, original_commit, end_commit)
        diffs = self.get_diffs()

        for index in range(len(comments)):
            if index < len(diffs):
                comments[index].diff = diffs[index]
        return comments

    def create_log(self, repo):
        subprocess.call(LOG_SH.format(repo), shell=True, stdout=subprocess.PIPE)

    def create_dif(self, repo, branch, begin_commit, end_commit):
        subprocess.call(DIFF_SH.format(repo, begin_commit, end_commit), shell=True, stdout=subprocess.PIPE)

    def get_diffs(self):
        diffs = []
        string = ''
        with open(FILENAME_DIFF, 'r') as file:
            lines = file.readlines()
            for i in lines:

                if i[0] in [PLUS, MINUS] and not i.startswith(PLUS * 3) and not i.startswith(MINUS * 3):
                    string = '%s%s' % (string, i)
                    continue
                if string:
                    diffs.append(string)
                string = ''
            return diffs

    def get_list_of_commit(self):
        with open(FILENAME_LOG, 'r') as file:
            commits = [i.split()[0] for i in file.readlines()]
            return commits

    def find_next_commit(self, prev_commit):
        next_commit = ''
        for commit in self.get_list_of_commit():
            if commit == prev_commit:
                return next_commit
            next_commit = commit
