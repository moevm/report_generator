import json
from app import ABS_PATH
from shutil import copyfile

JSON_FILE = ABS_PATH.format('settings.json')
DEFAULT_SETTINGS = ABS_PATH.format('default_settings.json')

LEN_COURSE_DOC = 33
LEN_LAB_DOC = 24
TYPE = "type"
LR = "LR"
KR = "KR"
EMPTY_DOC = "-"
MAIN_TEXT = "main_text"
CODE_TEXT = "code_text"
FONT = "font"
SIZE = "size"
NEW_MAIN_FONT = "general_font"
NEW_MAIN_SIZE = "general_size"
NEW_CODE_FONT = "code_font"
NEW_CODE_SIZE = "code_size"
NUMBER_FOR_H1 = 1
NUMBER_FOR_H6 = 7
HEADER = "h{}"
FORMAT = "format"
TEACHER = "teacher"
STUDENT = "student"
OLD_GROUP = "group"
NEW_GROUP = "number_group"
THEME = "theme"
CATHEDRA = "cathedra"
DISCIPLINE = "discipline"
OLD_CONTENT = "context_of_explanation"
NEW_CONTENT = "content"
MIN_PAGES = "min_pages"
DATE_START = "date_start"
DATE_FINISH = "date_finish"
DATE_DEFEND = "date_defend"
DOWNLOAD = "download"
PDF = "PDF"
COMMA = ","
COLON = ": "
STANDART_SIZE = 14
MAX_SIZE = 100
PAGES = 'pages'
PAGES_OF_WIKI = 'pages_of_wiki'
REPO = "repo_name"
GIT_SSH = 15
END_GIT = -4
NUMBER_PR = 'number_of_pr'
PR = 'pull_request'
OWNER = 'owner'
SET_REPO = 'repo'


class JsonApi:

    def __init__(self, new_dict):
        self.set_default()
        self.read_json_file()
        self.info_repo = new_dict[REPO][GIT_SSH:END_GIT].split('/')
        self.new_settings = new_dict
        self.change_content()
        self.write_json_file()

    def set_default(self):
        copyfile(DEFAULT_SETTINGS, JSON_FILE)

    def read_json_file(self):
        with open(JSON_FILE, 'r', encoding="utf-8") as file:
            self.json_data = json.load(file)

    def write_json_file(self):
        with open(JSON_FILE, 'w', encoding="utf-8") as file:
            file.write(json.dumps(self.json_data, sort_keys=False, indent=4, ensure_ascii=False,
                                  separators=(COMMA, COLON)))

    def change_content(self):
        length_set = len(self.new_settings)
        print(length_set)
        if length_set == LEN_COURSE_DOC:
            self.json_data[TYPE] = KR
            self.course_content()
        elif length_set == LEN_LAB_DOC:
            self.json_data[TYPE] = LR
            self.lab_content()
        else:
            print('EMPTY DOCUMENT')
            self.json_data[TYPE] = EMPTY_DOC
        self.general_content()

    def create_pages(self, pages):
        return pages.split(',')

    def general_content(self):
        if self.new_settings['number']: self.json_data['number'] = self.new_settings['number']

        if NUMBER_PR in self.new_settings and self.new_settings[NUMBER_PR]:
            self.json_data[PR][NUMBER_PR] = [int(self.new_settings[NUMBER_PR])]
            self.json_data[PR][OWNER] = self.info_repo[0]
            self.json_data[PR][SET_REPO] = self.info_repo[1]
        else:
            self.json_data[PR][NUMBER_PR] = []
        if self.new_settings[NEW_MAIN_FONT]: self.json_data[MAIN_TEXT][FONT] = self.new_settings[NEW_MAIN_FONT]
        if self.new_settings[NEW_MAIN_SIZE]: self.json_data[MAIN_TEXT][SIZE] = self.get_size(
            int(self.new_settings[NEW_MAIN_SIZE]))
        if self.new_settings[NEW_CODE_FONT]: self.json_data[CODE_TEXT][FONT] = self.new_settings[NEW_CODE_FONT]
        if self.new_settings[NEW_CODE_SIZE]: self.json_data[CODE_TEXT][SIZE] = self.get_size(
            int(self.new_settings[NEW_CODE_SIZE]))
        if self.new_settings[PAGES]:
            self.json_data[PAGES_OF_WIKI] = self.new_settings[PAGES].split(',')
        else:
            self.json_data[PAGES_OF_WIKI] = []

        if self.new_settings[DOWNLOAD]:
            self.json_data[DOWNLOAD] = self.new_settings[DOWNLOAD].split(',')
        else:
            self.json_data[DOWNLOAD] = []

        for i in range(NUMBER_FOR_H1, NUMBER_FOR_H6):
            if self.new_settings[HEADER.format(i)]:
                self.json_data[FORMAT][HEADER.format(i)][SIZE] = self.get_size(int(self.new_settings[HEADER.format(i)]))

    def get_size(self, size):
        if size < MAX_SIZE:
            return size
        return STANDART_SIZE

    def lab_content(self):
        if self.new_settings[TEACHER]: self.json_data[TEACHER] = self.new_settings[TEACHER]
        if self.new_settings[STUDENT]: self.json_data[STUDENT] = self.new_settings[STUDENT]
        if self.new_settings[NEW_GROUP]: self.json_data[OLD_GROUP] = self.new_settings[NEW_GROUP]
        if self.new_settings[THEME]: self.json_data[THEME] = self.new_settings[THEME]
        if self.new_settings[CATHEDRA]: self.json_data[CATHEDRA] = self.new_settings[CATHEDRA]
        if self.new_settings[DISCIPLINE]: self.json_data[DISCIPLINE] = self.new_settings[DISCIPLINE]
        if self.new_settings[PDF]:
            self.json_data[PDF] = True if self.new_settings[PDF] == "True" else False

    def course_content(self):
        self.lab_content()
        if self.new_settings[MIN_PAGES]: self.json_data[MIN_PAGES] = self.new_settings[MIN_PAGES]
        if self.new_settings[DATE_START]: self.json_data[DATE_START] = self.new_settings[DATE_START]
        if self.new_settings[DATE_FINISH]: self.json_data[DATE_FINISH] = self.new_settings[DATE_FINISH]
        if self.new_settings[DATE_DEFEND]: self.json_data[DATE_DEFEND] = self.new_settings[DATE_DEFEND]
        if self.new_settings['annotation']: self.json_data['annotation'] = self.new_settings['annotation']
        if self.new_settings['en_annotation']: self.json_data['en_annotation'] = self.new_settings['en_annotation']
        if self.new_settings['list_of_source'] : self.json_data['list_of_source'] = self.new_settings['list_of_source']
        if self.new_settings['context_of_explanation']: self.json_data['context_of_explanation'] = self.new_settings[
            'context_of_explanation']
        if self.new_settings['init_data']: self.json_data['init_data'] = self.new_settings['init_data']
