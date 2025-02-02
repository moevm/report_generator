#!./venv/bin/python3.6
import subprocess
import git
import requests
import os

from app import ABS_PATH
from github import Github
from github import GithubException
from information import get_oauth

LOCAL_REPO = ABS_PATH.format("repo_for_report")
LOCAL_WIKI = ABS_PATH.format("wiki_dir")
BEGIN_SSH = "git@github.com:{}"
SIZE_OF_SSH_ADDRESS = 19
COMMIT_MESSAGE = 'add report'
ORIGIN = 'origin'
STANDART_BRANCH = 'master'
ERROR_WIKI = "Не удалось получить доступ к wiki, проверьте ссылку"
ERROR_REPO = "Не удалось получить доступ к репозиторию, проверьте ссылку"
ERROR_BRANCH = "Не удалось найти ветку с таким названием"
ERROR_PUSH = 'this file has been in repository yet'
NEW_FILENAME = '{}{}.pdf'
LEN_PDF = 4
GEN_PATH_REPORT = '{}/{}'

INVITE_PATH = 'user/repository_invitations'
API = 'https://api.github.com/{}'
INVITE_URL = 'url'

API_GITHUB = "https://api.github.com/repos/{}/{}/pulls/{}/comments"
POSITION = "original_position"
USER = "user"
LOGIN = "login"
BODY = "body"
COMMIT = "original_commit_id"
DIFF_HUNK = "diff_hunk"
COMMENT_FILENAME = "path"
FILENAME_DIFF = ABS_PATH.format("diff_file.txt")
FILENAME_LOG = ABS_PATH.format("log_file.txt")
LOG_SH = ABS_PATH.format("do_git_log.sh {}")
DIFF_SH = ABS_PATH.format("do_git_diff.sh {} {} {}")
PLUS = "+"
MINUS = "-"


class Gengit:

    def __init__(self, ssh_url="", branch=STANDART_BRANCH):
        check_invites()
        self.url = ssh_url
        self.local_repo = LOCAL_REPO
        self.local_wiki = LOCAL_WIKI
        self.branch = branch
        if not branch:
            self.branch = STANDART_BRANCH
        self.repo = None

    # DOWNLOAD_GIT
    # def download_git(self):
    #     os.system(f"mkdir {self.local_repo}")
    #     return True
    #     try:
    #         self.repo = git.Repo.clone_from(self.url, self.local_repo)
    #     except git.GitCommandError as e:
    #         print(e.command)
    #         print(ERROR_REPO)
    #         raise ValueError(ERROR_REPO)
    #
    #     try:
    #         self.repo.git.checkout(self.branch)
    #     except git.GitCommandError as e:
    #         print(e.command)
    #         print(ERROR_BRANCH)
    #         raise ValueError(ERROR_BRANCH)

    def download_git_wiki(self):
        git_url = BEGIN_SSH.format(self.url[SIZE_OF_SSH_ADDRESS:])
        # git_url = self.url[:-3]+'wiki.git'
        print(git_url)
        try:
            self.repo = git.Repo.clone_from(git_url, self.local_wiki)
        except git.GitCommandError as e:
            print(e.command)
            print(ERROR_WIKI)
            raise ValueError(ERROR_WIKI)

    def add(self, filename):
        try:
            self.repo.index.add([filename])
            self.repo.index.commit(COMMIT_MESSAGE)
        except git.GitCommandError as e:
            print(e.command)

    def push(self, filename=''):
        path = GEN_PATH_REPORT.format(LOCAL_REPO, filename)
        my_github = Github(get_oauth())
        content = ''
        with open(path, 'rb') as file:
            content = file.read()
        repo = my_github.get_repo(self.url[15:-4])
        try:
            repo.create_file(filename, COMMIT_MESSAGE, content, branch=self.branch)
        except GithubException:
            contentfile = repo.get_contents(filename, ref=self.branch)
            repo.update_file(contentfile.path, COMMIT_MESSAGE, content, contentfile.sha, branch=self.branch)

        return filename

    def get_response(self, url):
        params = {"sort": "updated"}
        response = requests.get(url, params=params, headers=get_header())
        return response

    def comporator(self, object):
        return object[POSITION]

    def new_hunk(self, diff_string, start_line):
        new_str = diff_string.split('\n')[start_line:]
        return '\n'.join(new_str)

    def create_comments_for_word(self, my_json):
        mylist = []
        my_json = sorted(my_json, key=self.comporator)
        for comment in my_json:
            if comment["start_line"] is None:
                start_line = comment["original_start_line"]
            else:
                start_line = comment["start_line"]
            mylist.append([comment[POSITION], comment[USER][LOGIN], comment[BODY],
                           self.new_hunk(comment[DIFF_HUNK], start_line), comment[COMMIT],
                           comment[COMMENT_FILENAME]])
        return mylist

    class comment:
        def __init__(self, id):
            self.body_comments = []
            self.id = id
            self.body_code = ""
            self.commit = ""
            self.diff = ""
            self.filename = ""

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
            my_comment.filename = element[5]
            total_comments.append(my_comment)
        return total_comments

    def get_comments(self, company, name_of_repo, pull_requests):
        comments = []
        for number_of_pr in pull_requests:
            url = API_GITHUB.format(company, name_of_repo, number_of_pr)
            response = self.get_response(url)
            comments += self.create_comments_for_word(response.json())
        main_comments = self.optimization_comments(comments)
        return main_comments

    # def add_diff(self, comments, original_commit):
    #     self.create_log(self.local_repo)
    #     end_commit = self.find_next_commit(original_commit)
    #     self.create_dif(self.local_repo, self.branch, original_commit, end_commit)
    #     diffs = self.get_diffs()
    #     for index in range(len(comments)):
    #         if index < len(diffs):
    #             comments[index].diff = diffs[index]
    #     return comments

    def create_log(self, repo):
        subprocess.call(LOG_SH.format(repo), shell=True, stdout=subprocess.PIPE)

    # def create_dif(self, repo, branch, begin_commit, end_commit):
    #     subprocess.call(DIFF_SH.format(repo, begin_commit, end_commit), shell=True, stdout=subprocess.PIPE)
    #
    # def get_diffs(self):
    #     diffs = []
    #     string = ''
    #     with open(FILENAME_DIFF, 'r', encoding='utf-8') as file:
    #         lines = file.readlines()
    #         for i in lines:
    #             if i.find('diff --git a/README.md') != -1:
    #                 return diffs
    #             if i.startswith(PLUS * 3) or i.startswith(MINUS * 3):
    #                 continue
    #             if i[0] in [PLUS, MINUS]:
    #                 string = '%s%s' % (string, i)
    #                 continue
    #             if string:
    #                 diffs.append(string)
    #             string = ''
    #         return diffs

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


def get_header():
    return {'Authorization': 'token {}'.format(get_oauth())}


def get_requests(path, full_path=False):
    if not full_path:
        return requests.get(API.format(path), headers=get_header()).json()
    else:
        return requests.patch(path, headers=get_header())


def accept_invite(invite):
    get_requests(invite, full_path=True)


def get_invites():
    return get_requests(INVITE_PATH)


def check_invites():
    for invite in get_invites():
        accept_invite(invite[INVITE_URL])
