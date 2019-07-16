#!../venv/bin/python3.6
import argparse
import sys
import os
import shutil
from github_api import Gengit, LOCAL_REPO, LOCAL_WIKI
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
LINK = "https://github.com/{}/blob/{}/{}"
VAR_CONTENT = 3
EMPTY_PLACE = ""


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(FLAG_ARG)
    return parser


def input_cmd():
    url = input(INPUT_URL_MESSAGE)
    wiki_url = input(INPUT_WIKI_URL_MESSAGE)
    branch = input(INPUT_BRANCH_MESSAGE)
    return url, wiki_url, branch


def delete_dirs_and_files(git_local_repo=LOCAL_REPO, git_local_wiki=LOCAL_WIKI):
    if os.path.exists(git_local_repo):
        shutil.rmtree(git_local_repo)
    if os.path.exists(git_local_wiki):
        shutil.rmtree(git_local_wiki)
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
    delete_dirs_and_files()
    all_ok = True
    url, wiki_url, branch = type_of_input[0], type_of_input[1], type_of_input[2]
    git = Gengit(url, branch)
    git_wiki = Gengit(wiki_url)

    if git.download_git() is False or git_wiki.download_git_wiki() is False:
        delete_dirs_and_files()
        all_ok = False
    report = TIME_REPORT

    if all_ok:
        word = Dword(branch=branch)
        path_doc = os.path.join(git.local_repo, TIME_REPORT)
        word.save(path_doc)
        if word.js_content[PDF]:
            word.convert_to_pdf(docname=path_doc)
            report = PDF_EXTENSION.format(TIME_REPORT[:-LEN_WORD_EXTENSION])
        git.add(report)
        git.push()
        delete_dirs_and_files()
        return LINK.format(url[15:-4], branch, report)
    return EMPTY_PLACE


if __name__ == "__main__":
    parser = create_parser()
    namespace = parser.parse_args()

    if not namespace.f:
        main(input_cmd())
    else:
        main(input_file(namespace.f))

