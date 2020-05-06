'''
from github_oauth import Github

GITHUB = None


def getGithub():
    global GITHUB
    if GITHUB is None:
        GITHUB = Github()
    return GITHUB
'''
