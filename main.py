#!/usr/bin/env python3
from mygithub import *
from word import *
#import docx
#from docx import *
import shutil

d=Document()
login = input('login: ')
password = input('password: ')
url = input('url of repo: ')
branch = input('branch: ')
#print('login='+login+' password='+password+'url='+url+'test_branch='+branch)
git = gengit(login, password, url, branch)
wiki = git.checkwiki()
if wiki is not None:
    #git.downloadgit('https://github.com/light5551/test_gen.git')
    git.downloadgit()
#print(wiki)
word = dword()
#word.addcode(word.js['download'])
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



