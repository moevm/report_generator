#!/usr/bin/env python3
import sys,os
sys.path.append(os.getcwd()+'/venv/lib64/python3.6/site-packages')
from docx import Document
#import docx
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Pt
from pathlib import Path
import os
from docxtpl import DocxTemplate, RichText
import json
import subprocess
class dword():
    def __init__(self):
        self.maketitul()
        self.document = Document('generated_doc.docx')
        pass

    def convertpdf(self,docname):
        try:
            subprocess.check_call(
                ['/usr/bin/python3', '/usr/bin/unoconv', '-f', 'pdf', docname])
        except subprocess.CalledProcessError as e:
            print('CalledProcessError', e)
        pass
    def save(self,name='report.docx'):
        self.document.save(name)
        pass
    def addcode(self,filename):
        print(filename)
        path = next(Path(os.getcwd()).rglob(filename))
        print(path)
        f = open(str(path))
        code = f.read()
        f.close()
        #print(code)
        self.document.add_paragraph(code)
        pass

    def addLine(self, line):
        self.document.add_paragraph(line)
    def maketitul(self):
        doc = DocxTemplate("test_tml.docx")
        #self.js = json.load(open('settings.json'))
        self.js=json.load(open('mytestproject/settings.json'))
        context = {
                   'cathedra': RichText(self.js['cathedra']),
                   'discipline': RichText(self.js['discipline']),
                   'number': RichText(self.js['number']),
                   'theme': RichText(self.js['theme']),
                   'group': RichText(self.js['group']),
                   'student': RichText(self.js['student']),
                   'teacher': RichText(self.js['teacher']),
                   'sense': RichText(self.js['sense of work'])
                   }
        doc.render(context)
        doc.save("generated_doc.docx")
        pass

pass
