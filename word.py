#!./venv/bin/python3.6
import sys
import os
import json
import re
import subprocess
import requests
from pathlib import Path
from PIL import Image
from docx import Document
from docx.oxml.shared import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml.shared import qn
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Inches
from docxtpl import DocxTemplate, RichText


NAME_REPORT = "report.docx"
LOCAL_REPO = "generated_doc.docx"
SETTINGS_FILE = "settings.json"
COURSE_WORK = "KR"
LAB_WORK = "LR"
PATH_TO_TEMPLATE = "templates/{}.docx"
TYPE_OF_WORK = "type"
NOT_VALID = "not valid file"
MD_EXTENSION = ".md"
DICT_FILENAMES = 'download'
NO_FILE_MESSAGE = "No such file {}"
STYLE = "NORMAL {}"
STANDART_FONT = "Times New Roman"
STANDART_FONT_SIZE = 14
STANDART_PLACE_BEFORE = 0
STANDART_PLACE_AFTER = 0
STANDART_LINE_SPACING = 1.5
STANDART_FONT_QUOTE = "calibri"
ALIGN_CENTRE = "centre"
ALIGN_JUSTIFY = "justify"
ALIGN_LEFT = "left"
UNDER_PICTURE = "Рисунок {}{}"
ATTACHMENT = "Приложение"
PICTURE = "picture"
PAGES = "pages_of_wiki"
STANDART_SIZE_PICTURE = 4
BORDER_OF_PICTURE = 1.5
SPEED_OF_REDUCING_PICTURE = 0.8
DOT = "."
FONT_SIZE_CODE = 10
FONT_CODE = 'Consolas'

M_STUDENT = "Студент"
W_STUDENT = "Студентка"
M_W = "M/W"
MAN = "M"
MAN_OR_WOMAN = "manorgirl"
NUMBER = "number"
CATHEDRA = "cathedra"
DISCIPLINE = "discipline"
THEME = "theme"
GROUP = "group"
NAME_OF_STUDENT = "student"
TEACHER = "teacher"
INIT_DATA = "init_data"
CONTEXT_OF_EXPLANATION = "context_of_explanation"
MIN_PAGES = "min_pages"
DATE_START = "date_start"
DATE_FINISH = "date_finish"
DATE_DEFEND = "date_defend"
ANNOTATION = "annotation"
INTRODUCTION = "introduction"

ERROR_MESSAGE_UNOCONV = "Unoconv error: "
UNOCONC_1ST = "/usr/bin/python3"
UNOCONC_2ND = "/usr/bin/unoconv"
UNOCONC_3RD = "-f"
UNOCONC_4TH = "pdf"


SET_HEAD = "h{}"
LEFT_BRACKET = "["
RIGHT_BRACKET = "]"
RIGHT_BRACKET_V2 = ")"
HASH = "#"
CODE_SYMBOL = "`"
QUOTE_SYMBOL = ">"
LIST_SYMBOL = "•"
BOLD_SYMBOL = "*"
EXCLAMATION_MARK = "!"
ITALIC_SYMBOL = ["*", "_"]
EMPTY_PLACE = " "
EMPTY_STRING = ""

FORMAT = "format"
SET_CODE = "code"
FONT = "font"
SIZE = "size"

italic = False
bold = False
code = False
header = False
quote = False
lvl_head = 0
property_font = {0: italic, 1: bold, 2: code, 3: header, 4: quote}
ITALIC = 0
BOLD = 1
CODE = 2
HEADER = 3
QUOTE = 4

W_HYPERLINK = "w:hyperlink"
R_ID = "r:id"
W_R = "w:r"
W_RPR = "w:rPr"

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
        self.add_final_part()
        self.save(self.name)

    def add_page_break(self):
        self.doc.add_page_break()

    def download_settings(self):
        with open(SETTINGS_FILE) as file:
            self.js_content = json.load(file)

    def choose_path_template(self):
        if (self.js_content[TYPE_OF_WORK] == COURSE_WORK):
            self.path = PATH_TO_TEMPLATE.format(COURSE_WORK)
        if (self.js_content[TYPE_OF_WORK] == LAB_WORK):
            self.path = PATH_TO_TEMPLATE.format(LAB_WORK)

    def h_w(self, dimension):
        height, width = dimension
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
                [UNOCONC_1ST, UNOCONC_2ND, UNOCONC_3RD, UNOCONC_4TH, docname])
        except subprocess.CalledProcessError as e:
            print(ERROR_MESSAGE_UNOCONV, e)

    def save(self, name=NAME_REPORT):
        self.doc.save(name)

    def add_code(self):
        for filename in self.js_content[DICT_FILENAMES]:
            p = Path(os.getcwd()).rglob(filename)
            for path in p:
                code = NOT_VALID
                with open(path) as file:
                    if file is not None:
                        code = file.read()
                    else:
                        print(NO_FILE_MESSAGE.format(path))

                self.add_line(filename, set_bold=True, align=ALIGN_LEFT) 
                self.add_line(code, line_spacing=1, align=ALIGN_LEFT, font_name=FONT_CODE, font_size=FONT_SIZE_CODE)

    def change_bool_property(self, boolean):
        if property_font[boolean] is True:
            property_font[boolean] = False
        else:
            property_font[boolean] = True

    def add_symbol(self, paragraph, symbol, level_for_head=0):
        tmp = paragraph.add_run(symbol)
        tmp.font.italic = property_font[ITALIC]
        tmp.font.bold = property_font[BOLD]
        tmp.font.name = STANDART_FONT
        tmp.font.size = Pt(STANDART_FONT_SIZE)
        if property_font[CODE]:
            tmp.font.name = self.js_content[FORMAT][SET_CODE][FONT]
            tmp.font.size = Pt(self.js_content[FORMAT][SET_CODE][SIZE])
            tmp.font.italic = True
            tmp.font.bold = False
        elif property_font[HEADER]:
            level = SET_HEAD.format(level_for_head)
            tmp.font.name = self.js_content[FORMAT][level][FONT]
            tmp.font.size = Pt(self.js_content[FORMAT][level][SIZE])
            tmp.font.bold = True
        elif property_font[QUOTE]:
            tmp.font.italic = True
            tmp.font.name = STANDART_FONT_QUOTE

    def add_hyperlink(self, paragraph, url, text):
        part = paragraph.part
        r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink = OxmlElement(W_HYPERLINK)
        hyperlink.set(qn(R_ID), r_id)
        new_run = OxmlElement(W_R)
        rPr = OxmlElement(W_RPR)
        new_run.append(rPr)
        new_run.text = text
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)

    def select_text_and_link(self, text, index):
        start_size = index
        alt_text = []
        link = []
        index += 1
        need_text = True
        while index < len(text) and text[index] != RIGHT_BRACKET_V2:
            while index < len(text) and text[index] != RIGHT_BRACKET and need_text:
                alt_text.append(text[index])
                index += 1
            if text[index] == RIGHT_BRACKET:
                index += 2
            need_text = False
            if index < len(text):
                link.append(text[index])
            index += 1
        return index - start_size, EMPTY_STRING.join(link), EMPTY_STRING.join(alt_text)

    def level_head(self, text, index):
        begin_index = index
        while text[index] == HASH:
            index += 1
        return index - begin_index

    def wiki_parser(self, paragraph, text):
        str_len = len(text)
        i = 0
        level_for_head = 0
        while i < str_len:
            if text[i] == "\\":
                self.add_symbol(paragraph, text[i + 1], level_for_head)
                i += 2
                continue
            elif text[i] == "\n":
                level_for_head = 0
                property_font[HEADER] = False
            elif text[i] == QUOTE_SYMBOL:
                self.change_bool_property(QUOTE)
                i += 1
            elif text[i] == HASH:
                level_for_head = self.level_head(text, i)
                paragraph = self.new_paragraph()
                self.change_bool_property(HEADER)
                i += level_for_head
            elif text[i] == BOLD_SYMBOL and i + 1 < str_len and text[i + 1] == BOLD_SYMBOL:  # проверка на жирный шрифт
                self.change_bool_property(BOLD)
                i += 2
                continue
            elif text[i] == BOLD_SYMBOL and i + 1 < str_len and text[i + 1] == EMPTY_PLACE and not property_font[ITALIC]:
                self.add_symbol(paragraph, LIST_SYMBOL)  # проверка на список
                i += 1
                continue
            elif text[i] in ITALIC_SYMBOL:  # проверка на курсив
                self.change_bool_property(ITALIC)
                i += 1
                continue
            elif text[i] == CODE_SYMBOL:  # проверка на блок кода
                self.change_bool_property(CODE)
                i += 1
                continue
            elif text[i] == LEFT_BRACKET:  # проверка на гиперссылку
                offset, link, alt_text = self.select_text_and_link(text, i)
                self.add_hyperlink(paragraph, link, alt_text)
                i += offset + 1
                continue
            elif text[i] == EXCLAMATION_MARK and i + 1 < str_len and text[i + 1] == LEFT_BRACKET:  # проверка на изображение
                offset, link, alt_text = self.select_text_and_link(text, i)
                i += offset + 2
                self.add_image_by_url(link)
                paragraph = self.new_paragraph()
                continue
            if i < str_len:
                self.add_symbol(paragraph, text[i], level_for_head)
            i += 1

    def new_paragraph(self, align=ALIGN_LEFT, line_space=STANDART_LINE_SPACING):
        paragraph = self.doc.add_paragraph()
        paragraph_format = paragraph.paragraph_format
        paragraph_format.alignment = alignment_dict.get(align)
        paragraph_format.keep_with_next = True
        paragraph_format.line_spacing_rule = line_space_dict.get(line_space)
        paragraph_format.keep_together = True
        return paragraph

    def add_main_text_from_wiki(self):
        for filename in self.js_content[PAGES]:
            paragraph = self.new_paragraph()
            gen_path = Path(os.getcwd()).rglob("{0}{1}".format(filename, MD_EXTENSION))
            for path in gen_path:
                with open(path) as file:
                    text = file.read()
                    self.wiki_parser(paragraph, text)

    def add_image_by_url(self, url):
        req = requests.get(url)
        filepath = os.path.join(os.getcwd(), PICTURE)
        with open(filepath, 'wb') as file:
            file.write(req.content)
        self.add_picture(filepath)

    def add_final_part(self):
        self.add_page_break()
        self.add_line(ATTACHMENT, set_bold=True, align=ALIGN_CENTRE)
        self.add_code()

    def add_line(self, line, space_after=STANDART_PLACE_AFTER, set_bold=False, font_name=STANDART_FONT,
                 keep_with_next=False, font_size=STANDART_FONT_SIZE, space_before=STANDART_PLACE_BEFORE,
                 line_spacing=STANDART_LINE_SPACING, align=ALIGN_JUSTIFY, keep_together=True):
        self.number_of_paragraph += 1
        style_name = STYLE.format(self.number_of_paragraph)
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
                font.name = STANDART_FONT
                font.size = Pt(STANDART_FONT_SIZE)

    def add_picture(self, path):
        paragraph = self.doc.add_paragraph()
        p_format = paragraph.paragraph_format
        p_format.alignment = alignment_dict.get(ALIGN_CENTRE)
        time_word = paragraph.add_run()

        im = Image.open(path)
        h, w = self.h_w(im.size)
        time_word.add_picture(path, width=Inches(h), height=Inches(w)) 
        self.add_line(UNDER_PICTURE.format(self.num_of_pictures, DOT), align=ALIGN_CENTRE, keep_together=True)
        self.num_of_pictures += 1

    def make_title(self):
        doc = DocxTemplate(self.path)
        if self.js_content[M_W] == MAN:
            mw = M_STUDENT
        else:
            mw = W_STUDENT
        content = {
            MAN_OR_WOMAN: RichText(mw),
            NUMBER: RichText(self.js_content[NUMBER]),
            CATHEDRA: RichText(self.js_content[CATHEDRA]),
            DISCIPLINE: RichText(self.js_content[DISCIPLINE]),
            THEME: RichText(self.js_content[THEME]),
            GROUP: RichText(self.js_content[GROUP]),
            NAME_OF_STUDENT: RichText(self.js_content[NAME_OF_STUDENT]),
            TEACHER: RichText(self.js_content[TEACHER]),
            INIT_DATA: RichText(self.js_content[INIT_DATA]),
            CONTEXT_OF_EXPLANATION: RichText(self.js_content[CONTEXT_OF_EXPLANATION]),
            MIN_PAGES: RichText(self.js_content[MIN_PAGES]),
            DATE_START: RichText(self.js_content[DATE_START]),
            DATE_FINISH: RichText(self.js_content[DATE_FINISH]),
            DATE_DEFEND: RichText(self.js_content[DATE_DEFEND]),
            ANNOTATION: RichText(self.js_content[ANNOTATION]),
            INTRODUCTION: RichText(self.js_content[INTRODUCTION])

        }
        doc.render(content)
        doc.save(self.name)

