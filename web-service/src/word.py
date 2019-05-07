#!./venv/bin/python3.6
import sys
import os
import json
import re
import subprocess
import itertools
from docx import Document
import mistune
from pathlib import Path
from PIL import Image
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt, Inches
from docxtpl import DocxTemplate, RichText
from github_api import Gengit

GIT_REPO = "wiki_dir"
PATH_TO_WIKI = "{}/{}.md"
NAME_REPORT = "report.docx"
LOCAL_REPO = "generated_doc.docx"
TEMPLATE = "template"
SETTINGS_FILE = "settings.json"
COURSE_WORK = "KR"
LAB_WORK = "LR"
PATH_TO_TEMPLATE = "word_templates/{}.docx"
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

NAME_STYLE = "Mystyle"
HEAD_STYLE = "Myheadstyle"
SPAN_TEXT = "p.add_run(\"{}\",style=\'{}\')\n"
SPAN_EMPHASIS = "{}.italic = True\n"
SPAN_DOUBLE_EMPHASIS = "{}.bold = True\n"
SPAN_CODE = "p = self.document.add_paragraph()\np.add_run(\"{}\")\np.style = 'BasicUserQuote'\np.add_run().add_break()\n"
SPAN_LINK = "{} ({})"
SPAN_HRULE = "self.document.add_page_break()\n"

BLOCK = "block"
BLOCK_MATH = 'block_math'
TOKEN_TYPE = "type"
TOKEN_TEXT = "text"
EMPTY = " "
DASH = "-"

LIST_ITEM = "p = self.document.add_paragraph('', style = 'BasicUserList')"
LIST = "{}\np.add_run().add_break()\n"
HEADER = "p = self.document.add_paragraph(text=\"{}\",style=\"{}\")\n"
ADD_PICTURE = "add_picture"
END_STR = ':")\n'
RUN_AND_BREAK = 'p.add_run().add_break()'
ADD_PARAGRAPH = "p = self.document.add_paragraph()"
CREATE_TABLE = "table = self.document.add_table(rows={}, cols={}, style = 'BasicUserTable')"
END_TABLE = 'self.document.add_paragraph().add_run().add_break()\n'
ONE_PART_OF_TABLE = "table.rows[{}].cells[{}].paragraphs[0]{}\n"
PLUS_STR = "{}{}"
H_STYLE = "my_header_{}"
FORMAT = "format"
FONT = "font"
SIZE = "size"
TYPE_OF_HEADER = "h{}"
ERROR_STYLE_IN_MD = "В Markdown файле есть стиль, который не поддерживается программой!"
DISTANCE_NUMBER_CODE = " "

COMMENTS_PR = "Комменатрии из пулл-реквестов"
PR = "pull_request"
OWNER_OF_PR = "owner"
REPO_OF_PR = "repo"
NUMBER_OF_PR = "number_of_pr"

alignment_dict = {'justify': WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
                  'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'centre': WD_PARAGRAPH_ALIGNMENT.CENTER,
                  'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
                  'left': WD_PARAGRAPH_ALIGNMENT.LEFT}

line_space_dict = {1: WD_LINE_SPACING.SINGLE,
                   2: WD_LINE_SPACING.DOUBLE,
                   1.5: WD_LINE_SPACING.ONE_POINT_FIVE,
                   0: WD_LINE_SPACING.EXACTLY}


class MathBlockGrammar(mistune.BlockGrammar):
    block_math = re.compile(r"^\$\$(.*?)\$\$", re.DOTALL)


class MathBlockLexer(mistune.BlockLexer):
    default_rules = [BLOCK_MATH] + mistune.BlockLexer.default_rules

    def __init__(self, rules=None, **kwargs):
        if rules is None:
            rules = MathBlockGrammar()
        super(MathBlockLexer, self).__init__(rules, **kwargs)

    def parse_block_math(self, m):
        self.tokens.append({TOKEN_TYPE: BLOCK_MATH, TOKEN_TEXT: m.group(1)})


class MarkdownWithMath(mistune.Markdown):
    def __init__(self, renderer, **kwargs):
        kwargs[BLOCK] = MathBlockLexer
        super(MarkdownWithMath, self).__init__(renderer, **kwargs)

    def output_block_math(self):
        return self.renderer.block_math(self.token[TOKEN_TEXT])


class PythonDocxRenderer(mistune.Renderer):
    def __init__(self, **kwds):
        super(PythonDocxRenderer, self).__init__(**kwds)
        self.table_memory = []
        self.img_counter = 0

    def get_document(self, doc):
        self.document = doc

    def header(self, text, level, raw):
        return HEADER.format(text[text.find("\"") + 1:text.rfind("\"")], H_STYLE.format(level))

    def paragraph(self, text):
        if ADD_PICTURE in text:
            return text
        add_break = '' if text.endswith(END_STR) else RUN_AND_BREAK
        return PLUS_STR.format('\n'.join((ADD_PARAGRAPH, text, add_break)), '\n')

    def list(self, body, ordered):
        return LIST.format(body)

    def list_item(self, text):
        return '\n'.join((LIST_ITEM, text))

    def table(self, header, body):
        number_cols = header.count('\n') - 2
        number_rows = int(len(self.table_memory) / number_cols)
        cells = [ONE_PART_OF_TABLE.format(i, j, self.table_memory.pop(0)[1:])
                 for i, j in itertools.product(range(number_rows), range(number_cols))]
        tmp = "\n".join([CREATE_TABLE.format(number_rows, number_cols)] + cells)
        return PLUS_STR.format(tmp, END_TABLE)

    def table_cell(self, content, **flags):
        self.table_memory.append(content)
        return content

    # SPAN LEVEL
    def text(self, text):
        return SPAN_TEXT.format(text, NAME_STYLE)

    def emphasis(self, text):
        return SPAN_EMPHASIS.format(text[:-1])

    def double_emphasis(self, text):
        return SPAN_DOUBLE_EMPHASIS.format(text[:-1])

    def block_code(self, code, language):
        code = code.replace('\n', '\\n')
        return SPAN_CODE.format(code)


    def link(self, link, title, content):
        return SPAN_LINK.format(content, link)

    def hrule(self):
        return SPAN_HRULE


class Dword:

    def __init__(self):
        self.num_of_pictures = 1
        self.number_of_paragraph = 0
        self.name = LOCAL_REPO
        self.download_settings()
        self.choose_path_template()
        #self.make_title()
        #self.doc = Document(self.name)
        self.add_text_from_wiki()
        #self.add_final_part()
        self.add_comments()
        self.save(self.name)

    def create_styles(self):
        styles = self.document.styles
        # стиль для обычного текста
        style = styles.add_style(NAME_STYLE, WD_STYLE_TYPE.CHARACTER)
        style.font.size = Pt(STANDART_FONT_SIZE)
        style.font.name = STANDART_FONT
        # стили для загаловков
        for i in enumerate(self.js_content[FORMAT]):
            style = styles.add_style(H_STYLE.format(i[0] + 1), WD_STYLE_TYPE.PARAGRAPH)
            style.font.size = Pt(self.js_content[FORMAT][TYPE_OF_HEADER.format(i[0] + 1)][SIZE])
            style.font.name = self.js_content[FORMAT][TYPE_OF_HEADER.format(i[0] + 1)][FONT]

    def add_text_from_wiki(self):
        self.document = Document(os.path.abspath(self.path))
        self.create_styles()
        tmp = []

        for path in self.js_content[PAGES]:
            with open(PATH_TO_WIKI.format(GIT_REPO, path.replace(EMPTY, DASH)), 'r', encoding="utf-8") as file:
                tmp.append(file.read())

        renderer = PythonDocxRenderer()
        renderer.get_document(self.document)
        try:
            exec(MarkdownWithMath(renderer=renderer)('\n'.join(tmp)))
        except SyntaxError:
            print(ERROR_STYLE_IN_MD)
        #self.document.save(os.path.abspath(NAME_REPORT))

    def create_comments_from_git(self):
        pass

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

    def add_line(self, line, space_after=STANDART_PLACE_AFTER, set_bold=False, font_name=STANDART_FONT,
                 keep_with_next=False, font_size=STANDART_FONT_SIZE, space_before=STANDART_PLACE_BEFORE,
                 line_spacing=STANDART_LINE_SPACING, align=ALIGN_JUSTIFY, keep_together=True):
        self.number_of_paragraph += 1
        style_name = STYLE.format(self.number_of_paragraph)
        paragraph = self.document.add_paragraph(line)
        paragraph.style = self.document.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
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

    def add_final_part(self):
        self.add_page_break()
        self.add_line(ATTACHMENT, set_bold=True, align=ALIGN_CENTRE)
        self.add_code()

    @staticmethod
    def convert_to_pdf(docname):
        try:
            subprocess.check_call(
                [UNOCONC_1ST, UNOCONC_2ND, UNOCONC_3RD, UNOCONC_4TH, docname])
        except subprocess.CalledProcessError as e:
            print(ERROR_MESSAGE_UNOCONV, e)

    def save(self, name=NAME_REPORT):
        self.document.save(os.path.abspath(name))

    def number_position(self, _number, code_size):
        max_len = len(str(code_size))
        number = str(_number)
        len_number = len(number)
        return PLUS_STR.format(DISTANCE_NUMBER_CODE * (max_len - len_number), number)

    def add_code(self):
        for filename in self.js_content[DICT_FILENAMES]:
            gen_path = Path(os.getcwd()).rglob(filename)
            for path in gen_path:
                code = NOT_VALID
                with open(path) as file:
                    code = file.readlines()
                self.add_line(filename, set_bold=True, align=ALIGN_LEFT)
                for number, line in enumerate(code, 1):
                    self.add_line(
                        DISTANCE_NUMBER_CODE.join((self.number_position(number, len(code)), line.strip('\n'))),
                        line_spacing=1, align=ALIGN_LEFT, font_name=FONT_CODE, font_size=FONT_SIZE_CODE)

    def add_page_break(self):
        self.document.add_page_break()

    def download_settings(self):
        with open(SETTINGS_FILE) as file:
            self.js_content = json.load(file)

    def choose_path_template(self):
        if self.js_content[TYPE_OF_WORK] == COURSE_WORK:
            self.path = PATH_TO_TEMPLATE.format(COURSE_WORK)
        elif self.js_content[TYPE_OF_WORK] == LAB_WORK:
            self.path = PATH_TO_TEMPLATE.format(LAB_WORK)
        else:
            self.path = PATH_TO_TEMPLATE.format(TEMPLATE)

    def add_comments(self):
        git = Gengit()
        self.add_page_break()
        self.add_line(COMMENTS_PR, align=ALIGN_CENTRE, set_bold=True)
        comments = git.get_comments(self.js_content[PR][OWNER_OF_PR], self.js_content[PR][REPO_OF_PR],
                         self.js_content[PR][NUMBER_OF_PR])

        for element in comments:
            for body_element in element.body_comments:
                self.add_line("{}:{}".format(body_element[0], body_element[1]), line_spacing=1)
            self.add_line(element.body_code, align=ALIGN_LEFT, font_size=12)
