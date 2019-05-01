import json
JSON_FILE = 'settings.json'
LEN_COURSE_DOC = 24
LEN_LAB_DOC = 19
'''
принцип определения вида отчета - кол-во полей определяет вид отчета, так как
пустой док < лабораторная < курсовая 
'''
'''
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
'''

class json_api:

    def __init__(self, new_dict):
        self.read_json_file()
        self.change_content(new_dict)
        self.write_json_file()
        pass

    def read_json_file(self):
        with open(JSON_FILE, 'r') as file:
            self.json_data = json.load(file)

    def write_json_file(self):
        with open(JSON_FILE, 'w') as file:
            file.write(json.dumps(self.json_data))

    def change_content(self, settings):
        length_set = len(settings)
        if length_set == LEN_COURSE_DOC:
            print("course")
        elif length_set == LEN_LAB_DOC:
            print("lab")
        else:
            print("empty")
        print(len(settings))

    def general_content(self):
        pass

    def lab_content(self):
        pass

    def course_content(self):
        pass

if __name__ == '__main__':
    app = json_api()

