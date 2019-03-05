#!/usr/bin/env python3
from mygithub import Gengit
from word import Dword
import shutil

def main():
    url = input('url of repo(ssh): ')
    wiki_url = input('wiki repo(http):')
    branch = input('branch: ')
    git = Gengit(url, branch)
    git_wiki = Gengit(wiki_url, '')


    git.downloadgit()
    git_wiki.downloadgitwiki()
    #print(wiki)
    word = Dword()
    name = 'ready_project.docx'
    path_cr = './'+git.local_repo+'/'+name
    word.save(path_cr)
    if word.js["PDF"]:
        word.convert_to_pdf(path_cr)
        git.add(name[:-5]+'.pdf')
    else:
        git.add(name)
    git.push()
    shutil.rmtree(git.local_repo)
    shutil.rmtree(git_wiki.local_wiki)

if  __name__ ==  "__main__" :
    main()


