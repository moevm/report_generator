#!./venv/bin/python3.6
import argparse
import sys
import os
import shutil
from mygithub import Gengit
from word import Dword


TIME_REPORT = "ready_project.docx"
READY_WORD = "generated_doc.docx"
FROM_CONSOLE = "cmd"
PDF = "PDF"
PDF_EXTENSION = "{}.pdf"
INPUT_URL_MESSAGE = "url of repo(ssh): "
INPUT_WIKI_URL_MESSAGE = "wiki repo(http): "
INPUT_BRANCH_MESSAGE = "branch: "
LEN_WORD_EXTENSION = 5
DELETE_WORD = False
DELETED_PICTURE = "picture"
FLAG_ARG = "-f"


VAR_CONTENT = 3

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(FLAG_ARG)
    return parser


def input_cmd():
    url = input(INPUT_URL_MESSAGE)
    wiki_url = input(INPUT_WIKI_URL_MESSAGE)
    branch = input(INPUT_BRANCH_MESSAGE)
    return url, wiki_url, branch


def delete_directories_and_files(git, git_wiki):
    if os.path.exists(git.local_repo):
        shutil.rmtree(git.local_repo)
    if os.path.exists(git.local_wiki):
        shutil.rmtree(git_wiki.local_wiki)
    if os.path.exists(READY_WORD) and DELETE_WORD:
        os.remove(READY_WORD)
    if os.path.exists(DELETED_PICTURE):
        os.remove(DELETED_PICTURE)


def input_file(name):
    with open(name) as file:
        content = file.readlines()
    content = [element.strip() for element in content]
    return content[:VAR_CONTENT]


def main(type_of_input):
    all_ok = True
    if type_of_input is FROM_CONSOLE:
        url, wiki_url, branch = input_cmd()
    else:
        url, wiki_url, branch = input_file(type_of_input)
    git = Gengit(url, branch)
    git_wiki = Gengit(wiki_url)

    if git.download_git() is False or git_wiki.download_git_wiki() is False:
        delete_directories_and_files(git, git_wiki)
        all_ok = False

    if all_ok:
        word = Dword()
        path_doc = os.path.join(git.local_repo, TIME_REPORT)
        word.save(path_doc)
        if word.js_content[PDF]:
            word.convert_to_pdf(docname=path_doc)
            git.add(PDF_EXTENSION.format(TIME_REPORT[:-LEN_WORD_EXTENSION]))
        else:
            git.add(TIME_REPORT)
        git.push()
        delete_directories_and_files(git, git_wiki)


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()

    if not namespace.f:
        main(FROM_CONSOLE)
    else:
        main(namespace.f)


