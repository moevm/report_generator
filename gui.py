#!./venv/bin/python3.6
from tkinter import *
from tkinter.messagebox import *
import main

GIT_FILE = "git_file"
TITLE = "REPORT GENERATOR"
START_SIZE = "600x300+300+250"
TEXT_LABEL_SSH = "Введите ssh ссылку на репозиторий:"
TEXT_LABEL_WIKI = "Введите ссылку на wiki-страничку:"
TEXT_LABEL_BRANCH = "Введите название вветки:"
SHORT_INSTRUCTION = "short instruction"
CONTROL = "control"
EXIT = "exit"
INFO_MSG = "info"
FONT = ("ubuntu", 15)
BIG_BUTTON = ("ubuntu", 20)
INFORMATION = "информация"
MAIN_BUTTON = "Запуск"
INFORMATION_TEXT = '''
some information
'''


class Application:

    def set_settings_of_main_window(self):
        self.root.title(TITLE)
        self.root.geometry(START_SIZE)

    def create_standart_elements(self):
        self.label_ssh = Label(self.root, text=TEXT_LABEL_SSH, font=FONT)
        self.ssh_entry = Entry(self.root)
        self.label_ssh.grid(row=0, column=0)
        self.ssh_entry.grid(row=0, column=1)

    def create_git_elements(self):
        self.label_wiki = Label(self.root, text=TEXT_LABEL_WIKI, font=FONT)
        self.label_branch = Label(self.root, text=TEXT_LABEL_BRANCH, font=FONT)
        self.wiki_entry = Entry(self.root)
        self.branch_entry = Entry(self.root)

        self.label_wiki.grid(row=1, column=0, sticky=E)
        self.wiki_entry.grid(row=1, column=1)
        self.label_branch.grid(row=2, column=0, sticky=E)
        self.branch_entry.grid(row=2, column=1)

        button = Button(self.root, text=MAIN_BUTTON, font=BIG_BUTTON, command=self.start_git)
        button.grid(row=4, column=1, sticky="ew")

    def start_git(self):
        with open(GIT_FILE, "w") as file:
            file.write("{0}\n{1}\n{2}".format(
                str(self.ssh_entry.get()),
                str(self.wiki_entry.get()),
                str(self.branch_entry.get())
           ))
        main.main(GIT_FILE)

    def create_menu(self):
        main_menu = Menu(self.root)
        self.root.configure(menu=main_menu)

        first_item = Menu(main_menu, tearoff=0)
        second_item = Menu(main_menu, tearoff=0)

        main_menu.add_cascade(label=CONTROL, menu=first_item)
        first_item.add_command(label=EXIT, command=self.app_exit)

        main_menu.add_cascade(label=INFO_MSG, menu=second_item)
        second_item.add_command(label=SHORT_INSTRUCTION, command=self.get_info)

    def get_info(self):
        showinfo(INFORMATION, INFORMATION_TEXT)

    def app_exit(self):
        self.root.destroy()

    def __init__(self):
        self.root = Tk()
        self.set_settings_of_main_window()
        self.create_standart_elements()
        self.create_git_elements()
        self.create_menu()
        self.root.mainloop()


if __name__ == '__main__':
    app = Application()
