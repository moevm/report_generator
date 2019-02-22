#!/usr/bin/env python3
from mygithub import *
from word import *
#import docx
#from docx import *
import shutil

d=Document()
url = input('url of repo(ssh): ')
wiki_url = input('wiki repo(http):')
branch = input('branch: ')
#print('login='+login+' password='+password+'url='+url+'test_branch='+branch)
git = gengit(url, branch)
git_wiki = gengit(wiki_url, '')
git.downloadgit()
git_wiki.downloadgitwiki()
#print(wiki)
word = dword()
name = 'ready_project.docx'
path_cr = './'+git.local_repo+'/'+name
word.save(path_cr)
print("PDF IS "+str(word.js["PDF"]))
if word.js["PDF"]:
    word.convertpdf(path_cr)
    git.add(name[:-5]+'.pdf')
else:
    git.add(name)
git.push()
shutil.rmtree(git.local_repo)
shutil.rmtree(git_wiki.local_wiki)



