import json
JSON_FILE = 'settings.json'
LEN_COURSE_DOC = 24
LEN_LAB_DOC = 19
'''
принцип определения вида отчета - кол-во полей определяет вид отчета, так как
пустой док < лабораторной < курсовой 
'''

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
COMMA = ","
COLON = ": "


class JsonApi:

    def __init__(self, new_dict):
        self.read_json_file()
        self.new_settings = new_dict
        self.change_content()
        self.write_json_file()

    def read_json_file(self):
        with open(JSON_FILE, 'r') as file:
            self.json_data = json.load(file)

    def write_json_file(self):
        with open(JSON_FILE, 'w') as file:
            file.write(json.dumps(self.json_data, sort_keys=False, indent=4, ensure_ascii=False,
                                  separators=(COMMA, COLON)))

    def change_content(self):
        length_set = len(self.new_settings)
        if length_set == LEN_COURSE_DOC:
            self.json_data[TYPE] = KR
            self.course_content()
        elif length_set == LEN_LAB_DOC:
            self.json_data[TYPE] = LR
            self.lab_content()
        else:
            self.json_data[TYPE] = EMPTY_DOC
        self.general_content()

    def general_content(self):
        if self.new_settings[NEW_MAIN_FONT]: self.json_data[MAIN_TEXT][FONT] = self.new_settings[NEW_MAIN_FONT]
        if self.new_settings[NEW_MAIN_SIZE]: self.json_data[MAIN_TEXT][SIZE] = int(self.new_settings[NEW_MAIN_SIZE])
        if self.new_settings[NEW_CODE_FONT]: self.json_data[CODE_TEXT][FONT] = self.new_settings[NEW_CODE_FONT]
        if self.new_settings[NEW_CODE_SIZE]: self.json_data[CODE_TEXT][SIZE] = int(self.new_settings[NEW_CODE_SIZE])
        for i in range(NUMBER_FOR_H1, NUMBER_FOR_H6):
            if self.new_settings[HEADER.format(i)]:
                self.json_data[FORMAT][HEADER.format(i)][SIZE] = int(self.new_settings[HEADER.format(i)])

    def lab_content(self):
        if self.new_settings[TEACHER]: self.json_data[TEACHER] = self.new_settings[TEACHER]
        if self.new_settings[STUDENT]: self.json_data[STUDENT] = self.new_settings[STUDENT]
        if self.new_settings[NEW_GROUP]: self.json_data[OLD_GROUP] = self.new_settings[NEW_GROUP]
        if self.new_settings[THEME]: self.json_data[THEME] = self.new_settings[THEME]
        if self.new_settings[CATHEDRA]: self.json_data[CATHEDRA] = self.new_settings[CATHEDRA]
        if self.new_settings[DISCIPLINE]: self.json_data[DISCIPLINE] = self.new_settings[DISCIPLINE]

    def course_content(self):
        self.lab_content()
        if self.new_settings[NEW_CONTENT]: self.json_data[OLD_CONTENT] = self.new_settings[NEW_CONTENT]
        if self.new_settings[MIN_PAGES]: self.json_data[MIN_PAGES] = self.new_settings[MIN_PAGES]
        if self.new_settings[DATE_START]: self.json_data[DATE_START] = self.new_settings[DATE_START]
        if self.new_settings[DATE_FINISH]: self.json_data[DATE_FINISH] = self.new_settings[DATE_FINISH]
        if self.new_settings[DATE_DEFEND]: self.json_data[DATE_DEFEND] = self.new_settings[DATE_DEFEND]


if __name__ == '__main__':
    app = JsonApi()

