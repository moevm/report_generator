#!/usr/bin/env python3
import shutil
import argparse
import sys
from mygithub import Gengit
from word import Dword

TIME_REPORT = "ready_project.docx"
FROM_CONSOLE = "cmd"

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f')
    return parser

def input_cmd():
    url = input('url of repo(ssh): ')
    wiki_url = input('wiki repo(http):')
    branch = input('branch: ')
    return url, wiki_url, branch

def input_file(name):
    with open(name) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    return content[0], content[1], content[2]
    

def main(type_of_input):
    if type_of_input is FROM_CONSOLE:
        url, wiki_url, branch = input_cmd()
    else:
        url, wiki_url, branch = input_file(type_of_input)
    git = Gengit(url, branch)
    git_wiki = Gengit(wiki_url, '')

    git.downloadgit()
    git_wiki.downloadgitwiki()
    word = Dword()
    name = TIME_REPORT
    path_cr = "/".join((git.local_repo, name))
    word.save(path_cr)
    if word.js_content["PDF"]:
        word.convert_to_pdf(path_cr)
        git.add(name[:-5]+'.pdf')
    else:
        git.add(name)
    git.push()
    shutil.rmtree(git.local_repo)
    shutil.rmtree(git_wiki.local_wiki)

if  __name__ ==  "__main__" :
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.f is None:
        main(FROM_CONSOLE) 
    else:
        main(namespace.f)   
    


