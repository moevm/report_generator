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

# так мы указываем где лежат сторонние библиотеки
sys.path.append('{}/venv/lib64/python3.6/site-packages'.format(os.getcwd()))

NAME_REPORT = "report.docx"
LOCAL_REPO = "generated_doc.docx"
SETTINGS_FILE = "settings.json"
COURSE_WORK = "KR"
LAB_WORK = "LR"
PATH_TO_TEMPLATE = "templates/"
FILE_EXTENSION = ".docx"
NOT_VALID = "not valid file"
STANDART_SIZE_PICTURE = 4
BORDER_OF_PICTURE = 1.5
SPEED_OF_REDUCING_PICTURE = 0.8

alignment_dict = {'justify': WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
                  'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'centre': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
                  'left': WD_PARAGRAPH_ALIGNMENT.LEFT}

line_space_dict = {1: WD_LINE_SPACING.SINGLE,
                   2: WD_LINE_SPACING.DOUBLE,
                   1.5: WD_LINE_SPACING.ONE_POINT_FIVE,
                   0: WD_LINE_SPACING.EXACTLY}


class Dword:
    def __init__(self):
        self.num_of_pictures = 1
        self.number_of_paragraph = 0
        self.name = LOCAL_REPO
        self.download_settings()
        self.choose_path_template()
        self.make_title()
        self.doc = Document(self.name)
        self.add_main_text_from_wiki()
        self.convert_format()
        self.add_final_part()
        self.save(self.name)

    def add_page_break(self):
        self.doc.add_page_break()

    def download_settings(self):
        with open(SETTINGS_FILE) as file:
            self.js_content = json.load(file)

    def choose_path_template(self):
        self.path = PATH_TO_TEMPLATE
        if (self.js_content['type'] == COURSE_WORK):
            self.path += COURSE_WORK
        elif (self.js_content['type'] == LAB_WORK):
            self.path += LAB_WORK
        self.path += FILE_EXTENSION
#width , height
    def w_h(self, height, width):
        h = w = STANDART_SIZE_PICTURE
        if height > width:
            h *= height / width
            if h / w > BORDER_OF_PICTURE:
                while h / w > BORDER_OF_PICTURE:
                    h *= SPEED_OF_REDUCING_PICTURE
        else:
            w *= width / height
            if w / h > BORDER_OF_PICTURE:
                while w / h > BORDER_OF_PICTURE:
                    w *= SPEED_OF_REDUCING_PICTURE
        return h, w

    @staticmethod
    def convert_to_pdf(docname):
        try:
            subprocess.check_call(
                ['/usr/bin/python3', '/usr/bin/unoconv', '-f', 'pdf', docname])
        except subprocess.CalledProcessError as exc:
            print('CalledProcessError', exc)

    def save(self, name=NAME_REPORT):
        self.doc.save(name)

    def add_code(self):
        for filename in self.js_content['download']:
            path = next(Path(os.getcwd()).rglob(filename))
            # path = next(Path('.').rglob(filename))  # равносильные строчки(с верхней)
            code = NOT_VALID
            try:
                with open(str(path)) as file_:
                    if file_ is not None:
                        code = file_.read()
            except Exception:
                print("no such file {}".format(path))
            self.add_line(filename, set_bold=True, align='left')
            self.add_line(code, line_spacing=1, align='left', font_name='Consolas', font_size=10)

    # этот метод должен быть переделан - полностью!!!
    # эту функцию я не редактирую, потому что ее все равно надо будет удалить

    def add_main_text_from_wiki(self):
        firstpage = True
        for filename in self.js_content['pages_of_wiki']:

            if firstpage is False:
                self.add_page_break()
            firstpage = False
            path = next(Path(os.getcwd()).rglob(filename + '.md'))
            f = open(str(path))
            line = f.readlines()
            f.close()
            while '\n' in line:
                line.remove('\n')

            line = [str[:-1] for str in line]

            itr = iter(line)
            cur_line = next(itr)
            need_break = False
            while cur_line is not "":
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
                            self.add_line(mystr)
                            need_break = True
                            break

                    self.add_line(mystr)

                if need_break:
                    need_break = False
                    break

                if re.match(r'\*\*', cur_line) is not None:
                   self.add_line(cur_line[2:-2], set_bold=True, align='left', keep_with_next=True)
                #elif re.match(r'`', cur_line) is not None:
                #    self.add_code(cur_line)
                elif re.match(r'\**\*', cur_line) is not None:
                    self.add_line('•' + cur_line[1:], align='left', keep_with_next=True)
                elif re.match(r'!\[\]',cur_line) is not None:
                    self.add_image_by_url(cur_line[4:-1])
                try:
                    cur_line = next(itr)
                except:
                    break

    def add_image_by_url(self, url):
        req = requests.get(url)
        filepath = os.path.join(os.getcwd(), 'picture')
        with open(filepath, 'wb') as file_:
            file_.write(req.content)
        self.add_picture(filepath)

    def add_final_part(self):
        self.add_page_break()
        self.add_line('Приложение', set_bold=True, align='centre')
        self.add_code()

    def add_line(self, line, space_after=0, set_bold=False, font_name='Times New Roman', keep_with_next=False,
                 font_size=14, space_before=0, line_spacing=1.5, align='justify', keep_together=True):
        self.number_of_paragraph += 1
        style_name = 'Normal {}'.format(str(self.number_of_paragraph))
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
        for paragraph in self.doc.paragraphs:
            for run in paragraph.runs:
                font = run.font
                font.name = 'Times New Roman'       # в будущем этот параметр будет задоваться в settings.json
                font.size = Pt(14)

    def add_picture(self, filename):
        path = filename
        paragraph = self.doc.add_paragraph()
        p_format = paragraph.paragraph_format
        p_format.alignment = alignment_dict.get('centre')
        time_word = paragraph.add_run()

        im = Image.open(str(path))
        h, w = im.size
        h, w = self.w_h(h, w)
        time_word.add_picture(str(path), width=Inches(h), height=Inches(w))  # !!
        self.add_line('Рисунок {}{}'.format(self.num_of_pictures, '.'), align='centre', keep_together=True)
        self.num_of_pictures += 1

    def make_title(self):
        doc = DocxTemplate(self.path)
        if self.js_content['M/W'] == "M":
            mw = "Студент"
        else:
            mw = "Студентка"
        content = {
            'manorgirl': RichText(mw),
            'number': RichText(self.js_content['number']),
            'cathedra': RichText(self.js_content['cathedra']),
            'discipline': RichText(self.js_content['discipline']),
            'theme': RichText(self.js_content['theme']),
            'group': RichText(self.js_content['group']),
            'student': RichText(self.js_content['student']),
            'teacher': RichText(self.js_content['teacher']),
            'init_data': RichText(self.js_content['init_data']),
            'context_of_explanation': RichText(self.js_content['context_of_explanation']),
            'min_pages': RichText(self.js_content['min_pages']),
            'date_start': RichText(self.js_content['date_start']),
            'date_finish': RichText(self.js_content['date_finish']),
            'date_defend': RichText(self.js_content['date_defend']),
            'annotation': RichText(self.js_content['annotation']),
            'introduction': RichText(self.js_content['introduction'])

        }
        doc.render(content)
        doc.save(self.name)

