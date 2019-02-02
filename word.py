#!/usr/bin/env python3
import sys,os
sys.path.append(os.getcwd()+'/venv/lib64/python3.6/site-packages')
from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt
from docx.shared import Inches
from pathlib import Path
from PIL import Image
import os
from docxtpl import DocxTemplate, RichText
import json
import subprocess
alignment_dict = {'justify': WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
                  'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'centre': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
                  'left': WD_PARAGRAPH_ALIGNMENT.LEFT}

line_space_dict = {1: WD_LINE_SPACING.SINGLE,
                   2:  WD_LINE_SPACING.DOUBLE,
                   1.5:  WD_LINE_SPACING.ONE_POINT_FIVE,
                   0: WD_LINE_SPACING.EXACTLY}
class dword():
    def __init__(self):
        self.num_of_pictures = 1
        self.number_of_paragraph = 0
        self.name = 'generated_doc.docx'
        self.downloadwiki()
        self.choosepathoftemplate()
        self.maketitul()
        self.doc = Document(self.name)
        self.addmaintext()
        self.convert_format()
        self.addfinal()
        self.save(self.name)
        pass

    def addpagebreak(self):
        self.doc.add_page_break()

    def downloadwiki(self):
        self.js = json.load(open('mytestproject/settings.json'))

    def choosepathoftemplate(self):
        self.path = 'templates/'
        if(self.js['type'] == "KR"):
            self.path += "KR"
        elif(self.js['type'] == "LR"):
            self.path += "LR"
        self.path += ".docx"
        pass

    def w_h(self, width, height):
        h = w = 4
        if height > width:
            h *= height / width           
            if h/w > 1.5:
                while h/w >1.3:
                    h *= 0.8
        else:
            w *= width / height
            if w/h > 1.5:
                while w / h > 1.3:
                    w *= 0.8
        return (h,w)

    def convertpdf(self, docname):
        try:
            subprocess.check_call(
                ['/usr/bin/python3', '/usr/bin/unoconv', '-f', 'pdf', docname])
        except subprocess.CalledProcessError as e:
            print('CalledProcessError', e)
        pass

    def save(self,name = 'report.docx'):
        self.doc.save(name)
        pass

    def addcode(self,file = ""):
        if file is "":
            for filename in self.js['download']:
                path = next(Path(os.getcwd()).rglob(filename))
                code = 'not valid file'
                try:
                    f = open(str(path))
                    if f is not None:
                        code = f.read()
                    f.close()
                except Exception:
                    print("no such file"+str(path))
                self.addLine(filename,set_bold=True, align='left')
                self.addLine(code, line_spacing=1, align='left', font_name='Consolas', font_size=10)
        pass


    def addfinal(self):
        self.addpagebreak()
        self.addLine('Приложение', set_bold = True, align='centre', style_name='Normal'+str(self.number_of_paragraph))
        self.addcode()
        pass

    def addLine(self, line, space_after=0, set_bold=False, font_name='Times New Roman', keep_with_next=False, font_size=14, space_before=0, line_spacing=1.5, align='justify', keep_together = True, style_name=""):
        self.number_of_paragraph += 1
        style_name = 'Normal' + str(self.number_of_paragraph)
        paragraph = self.doc.add_paragraph(line)
        paragraph.style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        #style = self.doc.styles['Normal']
        font=paragraph.style.font
        #font = paragraph.style.font
        font.name = font_name
        font.size = Pt(font_size)
        font.bold = bool(set_bold)
        paragraph_format = paragraph.paragraph_format
        paragraph_format.alignment = alignment_dict.get(align.lower())
        paragraph_format.space_before = Pt(space_before)
        paragraph_format.space_after = Pt(space_after)
        paragraph_format.keep_with_next = keep_with_next
        paragraph_format.line_spacing_rule = line_space_dict.get(line_spacing)
        paragraph_format.keep_together = keep_together
        pass

    def convert_format(self):
        p = self.doc
        for paragraph in p.paragraphs:
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(14)
        pass

    def addPicture(self, filename):
        path = next(Path(os.getcwd()).rglob(filename))
        p = self.doc.add_paragraph()
        ##
        p_format = p.paragraph_format
        p_format.alignment = alignment_dict.get('centre')
        ##
        r = p.add_run()
        im = Image.open(str(path))
        (h, w) = im.size
        (h, w) = self.w_h(w,h)
        r.add_picture(str(path), width=Inches(h), height=Inches(w))#тут произошла какая-то путаница-но так правильно(потом  разобраться)
        self.addLine('Рисунок ' + str(self.num_of_pictures) + '.', align='centre', keep_together=True)
        self.num_of_pictures += 1

    def maketitul(self):
        doc = DocxTemplate(self.path)
        if self.js['M/W'] == "M":
            mw = "Студент"
        else:
            mw = "Студентка"
        content = {
                   'manorgirl': RichText(mw),
                   'number': RichText(self.js['number']),
                   'cathedra': RichText(self.js['cathedra']),
                   'discipline': RichText(self.js['discipline']),
                   'theme': RichText(self.js['theme']),
                   'group': RichText(self.js['group']),
                   'student': RichText(self.js['student']),
                   'teacher': RichText(self.js['teacher']),
                   'init_data': RichText(self.js['init_data']),
                   'context_of_explanation': RichText(self.js['context_of_explanation']),
                   'min_pages': RichText(self.js['min_pages']),
                   'date_start': RichText(self.js['date_start']),
                   'date_finish': RichText(self.js['date_finish']),
                   'date_defend': RichText(self.js['date_defend']),
                   'annotation': RichText(self.js['annotation']),
                   'introduction': RichText(self.js['introduction'])

                   }
        doc.render(content)
        doc.save(self.name)
        pass

    def addmaintext(self):
        p = self.js['content']
        for x in p:
            if (x['head'] is not ""):
                self.addLine('\t'+x['head'], space_after=0, set_bold=True,keep_together=True, keep_with_next=True,style_name='Normal'+str(self.number_of_paragraph), align='left')
            if (x['text'] is not ""):
                self.addLine(self.form(x['text']),keep_together=True, style_name='Normal'+str(self.number_of_paragraph))
            if (x['image'] is not ""):
                self.addPicture(x['image'])


    def form(self, text):#NEED TO FIX
        size = len(text)
        l = list(text)
        index = 0
        l.append(' ')
        if (l[0] is not '\t'):
            l.insert(index, '\t')
        index += 1
        while index <= size:
            #y = l[index]
            if l[index] is '$' and l[index+1] is '$':
                l.pop(index)
                l.pop(index)
                size -= 2
                while index < size and l[index] is not '$' and l[index+1] is not '$':
                    if l[index] is ' ':
                        l.pop(index)
                        l.insert(index,"\xa0")
                    index += 1
                l.pop(index+1)
                l.pop(index+1)
                size -= 2
            if l[index] is ',' or l[index] is '.':
                if l[index+1] is not ' ':
                    l.insert(index+1, ' ')
                    size += 1
                    index += 1

            if l[index] is ':' or l[index] is ';':
                l.insert(index+1, '\n')
                index += 1
                size += 1
            index += 1
        l.pop()
        return ''.join(l)
pass
