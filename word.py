#!/usr/bin/env python3
import sys
import os
import json
import re
import subprocess
import requests
from pathlib import Path
from PIL import Image
from docx import Document
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Inches
from docxtpl import DocxTemplate, RichText

sys.path.append(os.getcwd()+'/venv/lib64/python3.6/site-packages')

LOCAL_REPO = "generated_doc.docx"
SETTINGS_FILE = "settings.json"
COURSE_WORK = "KR"
LAB_WORK = "LR"
PATH_TO_TEMPLATE = "templates/"
FILE_EXTENSION = ".docx"

alignment_dict = {'justify': WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
                  'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'centre': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
                  'left': WD_PARAGRAPH_ALIGNMENT.LEFT}

line_space_dict = {1: WD_LINE_SPACING.SINGLE,
                   2: WD_LINE_SPACING.DOUBLE,
                   1.5: WD_LINE_SPACING.ONE_POINT_FIVE,
                   0: WD_LINE_SPACING.EXACTLY}


class Dword():
    def __init__(self):
        self.num_of_pictures = 1
        self.number_of_paragraph = 0
        #self.name = 'generated_doc.docx'
        self.name = LOCAL_REPO
        self.download_settings()
        # self.downloadwiki()
        self.choose_path_template()
        self.make_titul()
        self.doc = Document(self.name)
        # self.addmaintext()
        self.add_main_text_from_wiki()
        self.convert_format()
        self.addfinal()
        self.save(self.name)
        pass

    def add_page_break(self):
        self.doc.add_page_break()

    def download_settings(self):
        self.js = json.load(open(SETTINGS_FILE))

    def choose_path_template(self):
        self.path = PATH_TO_TEMPLATE
        if (self.js['type'] == COURSE_WORK):
            self.path += COURSE_WORK
        elif (self.js['type'] == LAB_WORK):
            self.path += LAB_WORK
        self.path += FILE_EXTENSION

    def w_h(self, width, height):
        h = w = 4
        if height > width:
            h *= height / width
            if h / w > 1.5:
                while h / w > 1.3:
                    h *= 0.8
        else:
            w *= width / height
            if w / h > 1.5:
                while w / h > 1.3:
                    w *= 0.8
        return (h, w)

    def convert_to_pdf(self, docname):
        try:
            subprocess.check_call(
                ['/usr/bin/python3', '/usr/bin/unoconv', '-f', 'pdf', docname])
        except subprocess.CalledProcessError as e:
            print('CalledProcessError', e)

    def save(self, name='report.docx'):
        self.doc.save(name)

    def add_code(self, file=""):
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
                    print("no such file" + str(path))
                self.addLine(filename, set_bold=True, align='left')
                self.addLine(code, line_spacing=1, align='left', font_name='Consolas', font_size=10)

    def add_main_text_from_wiki(self):
        pages = self.js['pages_of_wiki']
        firstpage = True
        for filename in self.js['pages_of_wiki']:

            if firstpage is False:
                self.add_page_break()
            firstpage = False
            #self.addpagebreak()
            path = next(Path(os.getcwd()).rglob(filename + '.md'))
            f = open(str(path))
            line = f.readlines()
            f.close()
            while '\n' in line:
                line.remove('\n')

            line = [str[:-1] for str in line]

            itr = iter(line)
            ########################################
            global cur_line
            cur_line = next(itr)
            global need_break
            need_break = False
            while (cur_line is not ""):
                #nonlocal cur_line
                if (re.match(r'\*\*', cur_line) is None and (re.match(r'`', cur_line) is None) and (
                        re.match(r'\*', cur_line) is None)):
                    mystr = ''
                    while (re.match(r'\*\*', cur_line) is None and (re.match(r'`', cur_line) is None) and (
                           re.match(r'\*', cur_line) is None) and cur_line is not "" and
                           re.match(r'!\[\]', cur_line) is None):
                        mystr +=' ' + cur_line
                        try:
                            cur_line = next(itr)
                        except:
                            self.addLine(mystr)
                           # self.addpagebreak()
                            need_break = True
                            break

                    self.addLine(mystr)

                if need_break:
                    need_break = False
                    break

                if (re.match(r'\*\*', cur_line) is not None):
                   self.addLine(cur_line[2:-2], set_bold=True, align='left',keep_with_next=True)
                elif (re.match(r'`', cur_line) is not None):

                    self.add_code(cur_line)
                elif (re.match(r'\**\*', cur_line) is not None):

                    self.addLine('•' + cur_line[1:], align='left', keep_with_next=True)
                elif (re.match(r'!\[\]',cur_line) is not None):
                    self.addimagebyurl(cur_line[4:-1])
                try:
                    cur_line = next(itr)
                except:
                    #self.addpagebreak()
                    break

    def addimagebyurl(self,url):
        r = requests.get(url)
        filepath = os.path.join(os.getcwd()+'/'+'picture')
        with open(filepath, 'wb') as f:
            f.write(r.content)
        self.addPicture(filepath)

    def addfinal(self):
        self.add_page_break()
        self.addLine('Приложение', set_bold=True, align='centre', style_name='Normal' + str(self.number_of_paragraph))
        self.add_code()

    def addLine(self, line, space_after=0, set_bold=False, font_name='Times New Roman', keep_with_next=False,
                font_size=14, space_before=0, line_spacing=1.5, align='justify', keep_together=True, style_name=""):
        self.number_of_paragraph += 1
        style_name = 'Normal' + str(self.number_of_paragraph)
        paragraph = self.doc.add_paragraph(line)
        paragraph.style = self.doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        font = paragraph.style.font
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

    def convert_format(self):
        p = self.doc
        for paragraph in p.paragraphs:
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'
                font.size = Pt(14)

    def addPicture(self, filename):
        path = filename
        p = self.doc.add_paragraph()
        p_format = p.paragraph_format
        p_format.alignment = alignment_dict.get('centre')
        r = p.add_run()
        im = Image.open(str(path))
        (h, w) = im.size
        (h, w) = self.w_h(w, h)
        r.add_picture(str(path), width=Inches(h),
                      height=Inches(w))  # тут произошла какая-то путаница-но так правильно(потом  разобраться)
        self.addLine('Рисунок ' + str(self.num_of_pictures) + '.', align='centre', keep_together=True)
        self.num_of_pictures += 1

    def make_titul(self):
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
